1. How is your application stateless, and what assumptions does it make about local state or persistence?
The application is stateless because each http request independent and past interactions are not saved in a server. The application assumes that the local state is given at the time of deployment, which means it will not have to rely on previous deployments for data.
2. What are cold starts, and how might they affect your application's latency or user experience?
A cold start is when an application mist prepare a new execution environment. Cold starts can drastically affect an applications latency as setting up application environments, starting runtime, and initializing code can be taxing and take lots of time.
3. How does FaaS scale for bursty HTTP workloads, and what operational work is handled by the provider instead of by you?
FaaS automatically scales to the number of http requests. The provider handles all work except for the user-defined functions.
4. What are the main benefits of using FaaS for this portfolio deployment?
FaaS is very fast, scales easily to the number of https requests, requires less maintenance by the user and is a much cheaper option compared to other cloud deployment methods.
5. What are the main limitations of FaaS for this portfolio and for more complex applications?
The main limitation of FaaS is limited control over preventing cold starts, specifically for the serverless website we have no control over the application environment, starting runtime and initializing code.
6. How does this deployment model differ operationally from the VM-based deployment in HW1?
This deployment method scaled automatically, required very low maintanence over computing resources and an http request triggered the applications deployment.
7. When is FaaS preferable to VMs or containers for this kind of workload, and when is it not a good fit?
FaaS is preferable when the user wants scalablity to be event driven, the overhead cost to be low, the user maintanence of computing resources to be low, and when control over cold starts is not a priority for the application.
