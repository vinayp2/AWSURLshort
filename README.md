# AWSURLshort

The code is referenced as notesApp due to it being created from that. 
this is code for a url shortener that was deployed on aws. it uses flask and mongodb. For deployment it used nginx and gunicorn with gunicorn operating on port 8000. Zookeeper was used as a counter to generate short urls that were then base 62 encoded. Zookeeper is assummed to be running on port 2181. This provides a /health for health checks done by a load balancer. it also has login/ logout functionality. 
