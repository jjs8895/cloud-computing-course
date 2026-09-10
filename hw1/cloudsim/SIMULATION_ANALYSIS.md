Cloudsim Analysis

Q1. Execution time
 - total simulation clock time: 
	400.01s 
 - Which cloudlet finished last, and why?
	Cloudley #0 finished last because it was the only cloudlet
 - Can cloudlets run in parallel under this configuration? Why or why not?
	No, the cloudlets cannot run in parallel under this configuration because there is only one cpu, VM, host an
	cloudlet

Q2. Resouce Utilization
 - How many Datacenter Hosts does this example initialize? How many processing cores are allocated per host?
	One host
 - How many Virtual Machines (VMs) are created? How many cores are given to each VM?
	One VM and one core

Q3. Task Scheduling
 - in what order did the cloudlet execute?
	Cloudlet #0 to VM 
	Cloudlet #0 Executes
	Cloudlet #0 execution finishes
	Total simulation clock time 400.01s 
 - What represents the primary performance bottleneck (CPU, memory, or network infastructure)?
	CPU

Q4. Real-World Analogy
 - How does this structural simulation mirror actual virtualized public cloud infastructure like Google Compute Engine
	Structural simulation mirrors actual virtualized public cloud infastructure like Google Compute Engine by having a server run the virtual machines that execute the cloudlets. This is similar to google compute engine which utilizes data centers that provides infastructure for the virtual machines that run customer applications.
 - What physical hardware or software abstractions map to Hosts, VMS and Cloudlets?
	Hosts map to the physical server
	Virtual machine maps to the host
	Cloudlets map to the virtual machine
