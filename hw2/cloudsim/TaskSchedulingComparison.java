import org.cloudbus.cloudsim.Cloudlet;
import org.cloudbus.cloudsim.CloudletSchedulerTimeShared;
import org.cloudbus.cloudsim.Datacenter;
import org.cloudbus.cloudsim.DatacenterBroker;
import org.cloudbus.cloudsim.DatacenterCharacteristics;
import org.cloudbus.cloudsim.Host;
import org.cloudbus.cloudsim.Log;
import org.cloudbus.cloudsim.Pe;
import org.cloudbus.cloudsim.Storage;
import org.cloudbus.cloudsim.UtilizationModel;
import org.cloudbus.cloudsim.UtilizationModelFull;
import org.cloudbus.cloudsim.Vm;
import org.cloudbus.cloudsim.VmAllocationPolicySimple;
import org.cloudbus.cloudsim.VmSchedulerTimeShared;
import org.cloudbus.cloudsim.core.CloudSim;
import org.cloudbus.cloudsim.provisioners.BwProvisionerSimple;
import org.cloudbus.cloudsim.provisioners.PeProvisionerSimple;
import org.cloudbus.cloudsim.provisioners.RamProvisionerSimple;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public class TaskSchedulingComparison {
    private static final int VM_COUNT = 3;
    private static final int HOST_COUNT = 2;

    private enum Policy {
        FCFS,
        SJF
    }

    private static final class WorkloadSpec {
        private final int id;
        private final long length;
        private final int pesNumber;
        private final long fileSize;
        private final long outputSize;

        private WorkloadSpec(int id, long length, int pesNumber, long fileSize, long outputSize) {
            this.id = id;
            this.length = length;
            this.pesNumber = pesNumber;
            this.fileSize = fileSize;
            this.outputSize = outputSize;
        }
    }

    public static void main(String[] args) {
        if (args.length != 2) {
            printUsage();
            return;
        }

        Policy policy;
        try {
            policy = Policy.valueOf(args[0].trim().toUpperCase(Locale.US));
        } catch (IllegalArgumentException error) {
            printUsage();
            return;
        }

        try {
            List<WorkloadSpec> workload = loadWorkload(args[1]);
            runSimulation(policy, workload);
        } catch (Exception error) {
            error.printStackTrace();
            Log.println("The simulation terminated because of an unexpected error.");
        }
    }

    private static void runSimulation(Policy policy, List<WorkloadSpec> workload) throws Exception {
        int numUsers = 1;
        Calendar calendar = Calendar.getInstance();
        boolean traceFlag = false;

        CloudSim.init(numUsers, calendar, traceFlag);

        createDatacenter("Datacenter_0");
        DatacenterBroker broker = new DatacenterBroker("Broker");
        int brokerId = broker.getId();

        List<Vm> vms = createVms(brokerId);
        List<Cloudlet> cloudlets = createCloudlets(brokerId, workload);

        broker.submitGuestList(vms);
        broker.submitCloudletList(cloudlets);

        if (policy == Policy.FCFS) {
            bindCloudletsFcfs(broker, cloudlets, vms);
        } else {
            bindCloudletsSjfLoadAware(broker, cloudlets, vms);
        }

        Log.println("Starting TaskSchedulingComparison with policy: " + policy);
        CloudSim.startSimulation();
        CloudSim.stopSimulation();

        List<Cloudlet> results = broker.getCloudletReceivedList();
        results.sort(Comparator.comparingInt(Cloudlet::getCloudletId));

        printCloudletList(results);
        printVmSummary(results, vms);
        printMakespan(results);
    }

    private static List<WorkloadSpec> loadWorkload(String workloadPath) throws IOException {
        List<WorkloadSpec> specs = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(new FileReader(workloadPath))) {
            String line;
            boolean headerConsumed = false;
            while ((line = reader.readLine()) != null) {
                String trimmed = line.trim();
                if (trimmed.isEmpty() || trimmed.startsWith("#")) {
                    continue;
                }

                if (!headerConsumed) {
                    headerConsumed = true;
                    if (trimmed.toLowerCase(Locale.US).startsWith("cloudlet_id")) {
                        continue;
                    }
                }

                String[] parts = trimmed.split(",");
                if (parts.length != 5) {
                    throw new IllegalArgumentException("Invalid workload row: " + line);
                }

                specs.add(
                    new WorkloadSpec(
                        Integer.parseInt(parts[0].trim()),
                        Long.parseLong(parts[1].trim()),
                        Integer.parseInt(parts[2].trim()),
                        Long.parseLong(parts[3].trim()),
                        Long.parseLong(parts[4].trim())
                    )
                );
            }
        }

        if (specs.isEmpty()) {
            throw new IllegalArgumentException("The workload file did not contain any cloudlets.");
        }

        return specs;
    }

    private static Datacenter createDatacenter(String name) {
        List<Host> hostList = new ArrayList<>();

        for (int hostIndex = 0; hostIndex < HOST_COUNT; hostIndex++) {
            List<Pe> peList = new ArrayList<>();
            peList.add(new Pe(0, new PeProvisionerSimple(1000)));
            peList.add(new Pe(1, new PeProvisionerSimple(1000)));

            hostList.add(
                new Host(
                    new RamProvisionerSimple(4096),
                    new BwProvisionerSimple(10000),
                    1_000_000,
                    peList,
                    new VmSchedulerTimeShared(peList)
                )
            );
        }

        DatacenterCharacteristics characteristics = new DatacenterCharacteristics(
            "x86",
            "Linux",
            "Xen",
            hostList,
            10.0,
            3.0,
            0.05,
            0.001,
            0.0
        );

        try {
            return new Datacenter(name, characteristics, new VmAllocationPolicySimple(hostList), new LinkedList<Storage>(), 0);
        } catch (Exception error) {
            throw new RuntimeException("Failed to create datacenter", error);
        }
    }

    private static List<Vm> createVms(int brokerId) {
        List<Vm> vms = new ArrayList<>();

        for (int vmId = 0; vmId < VM_COUNT; vmId++) {
            vms.add(
                new Vm(
                    vmId,
                    brokerId,
                    500,
                    1,
                    1024,
                    1000,
                    10000,
                    "Xen",
                    new CloudletSchedulerTimeShared()
                )
            );
        }

        return vms;
    }

    private static List<Cloudlet> createCloudlets(int brokerId, List<WorkloadSpec> workload) {
        List<Cloudlet> cloudlets = new ArrayList<>();
        UtilizationModel utilization = new UtilizationModelFull();

        for (WorkloadSpec spec : workload) {
            Cloudlet cloudlet = new Cloudlet(
                spec.id,
                spec.length,
                spec.pesNumber,
                spec.fileSize,
                spec.outputSize,
                utilization,
                utilization,
                utilization
            );
            cloudlet.setUserId(brokerId);
            cloudlets.add(cloudlet);
        }

        return cloudlets;
    }

    private static void bindCloudletsFcfs(DatacenterBroker broker, List<Cloudlet> cloudlets, List<Vm> vms) {
        for (int index = 0; index < cloudlets.size(); index++) {
            Cloudlet cloudlet = cloudlets.get(index);
            Vm vm = vms.get(index % vms.size());
            broker.bindCloudletToVm(cloudlet.getCloudletId(), vm.getId());
        }
    }

    private static void bindCloudletsSjfLoadAware(DatacenterBroker broker, List<Cloudlet> cloudlets, List<Vm> vms) {
        // TODO: Implement the required HW2 SJF load-aware policy.
        // 1. Sort the cloudlets by ascending cloudlet length.
        // 2. Track the total assigned cloudlet length per VM.
        // 3. For each cloudlet, bind it to the VM with the smallest current load.
        // 4. Break ties by choosing the VM with the lower VM ID.
        // 5. Call broker.bindCloudletToVm(cloudletId, vmId) for every cloudlet.
        
	Map<Integer, Long> vmAssignedLength = new LinkedHashMap<>();
	Vm temp_vm = null;
	Long length = 0L;

	cloudlets.sort(Comparator.comparingLong(Cloudlet::getCloudletLength));

	for (Vm vm : vms) {
		vmAssignedLength.put(vm.getId(), length);
	}

	for (int index = 0; index < cloudlets.size(); index++){
		Cloudlet cloudlet = cloudlets.get(index);
		temp_vm = null;
		for (Vm vm : vms) {
			if(temp_vm == null){
				temp_vm = vm;
			}
			else if(vmAssignedLength.get(vm.getId()) < vmAssignedLength.get(temp_vm.getId())){
				temp_vm = vm;
			}
	                else if(vmAssignedLength.get(vm.getId()).equals(vmAssignedLength.get(temp_vm.getId())) 
					&& vm.getId() < temp_vm.getId()){
				temp_vm = vm;
			}
		}
		broker.bindCloudletToVm(cloudlet.getCloudletId(), temp_vm.getId());
		vmAssignedLength.put(temp_vm.getId(), vmAssignedLength.get(temp_vm.getId()) 
				+ cloudlet.getCloudletLength());
	}


       // throw new UnsupportedOperationException("Implement bindCloudletsSjfLoadAware before running the sjf policy.");
    }

    private static void printCloudletList(List<Cloudlet> cloudlets) {
        DecimalFormat format = new DecimalFormat("###.##");
        String indent = "    ";

        Log.println();
        Log.println("========== OUTPUT ==========");
        Log.println(
            "Cloudlet ID" + indent +
            "STATUS" + indent +
            "Data center ID" + indent +
            "VM ID" + indent +
            "Time" + indent +
            "Start Time" + indent +
            "Finish Time"
        );

        for (Cloudlet cloudlet : cloudlets) {
            Log.print(indent + cloudlet.getCloudletId() + indent + indent);

            if (cloudlet.getStatus() == Cloudlet.CloudletStatus.SUCCESS) {
                Log.print("SUCCESS");
                Log.println(
                    indent + indent + cloudlet.getResourceId() +
                    indent + indent + indent + cloudlet.getGuestId() +
                    indent + indent + format.format(cloudlet.getActualCPUTime()) +
                    indent + indent + format.format(cloudlet.getExecStartTime()) +
                    indent + indent + format.format(cloudlet.getExecFinishTime())
                );
            }
        }
    }

    private static void printVmSummary(List<Cloudlet> cloudlets, List<Vm> vms) {
        Map<Integer, Long> vmAssignedLength = new LinkedHashMap<>();
        Map<Integer, Integer> vmCloudletCount = new LinkedHashMap<>();

        for (Vm vm : vms) {
            vmAssignedLength.put(vm.getId(), 0L);
            vmCloudletCount.put(vm.getId(), 0);
        }

        for (Cloudlet cloudlet : cloudlets) {
            int vmId = cloudlet.getGuestId();
            vmAssignedLength.put(vmId, vmAssignedLength.get(vmId) + cloudlet.getCloudletLength());
            vmCloudletCount.put(vmId, vmCloudletCount.get(vmId) + 1);
        }

        Log.println();
        Log.println("========== VM SUMMARY ==========");
        for (Vm vm : vms) {
            int vmId = vm.getId();
            Log.println(
                "VM " + vmId +
                " -> cloudlets=" + vmCloudletCount.get(vmId) +
                ", total_length=" + vmAssignedLength.get(vmId)
            );
        }
    }

    private static void printMakespan(List<Cloudlet> cloudlets) {
        double makespan = 0.0;
        for (Cloudlet cloudlet : cloudlets) {
            makespan = Math.max(makespan, cloudlet.getExecFinishTime());
        }

        DecimalFormat format = new DecimalFormat("###.##");
        Log.println();
        Log.println("Makespan: " + format.format(makespan));
    }

    private static void printUsage() {
        System.out.println("Usage: java TaskSchedulingComparison <fcfs|sjf> <workload.csv>");
    }
}
