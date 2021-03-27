# kubedog

Kubedog is an API that orchestrates various kubernetes operations.

The operations supported as of now is.

    a.Scheduling of kubernetes pods . Since most of us use kubernetes in our local dev machines . We end up seeing mounting costs . 
      So kubedog helps by scheduling the pods downtime. 
    b.kubedog simplifies the use of kubernetes by exposing API for kube crud operations
    c.kubedog should also stream logs via the API model . Since log streaming needs to be async, So we at kubedog are working on making the log steamer
      via some streaming source that can be configurable. 