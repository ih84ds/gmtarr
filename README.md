To get things working, the following local/private files need to be created:

* roundrobin/settings_local.py (copy and edit settings_local.py.template)
* SSL cert/key
  * docker/nginx/ssl/server.cert
  * docker/nginx/ssl/server.key
  * can generate self signed certificate/key from www.selfsignedcertificate.com for dev environment
