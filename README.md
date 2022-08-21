To get things working, the following local/private files need to be created:

* roundrobin/settings_local.py (copy and edit settings_local.py.template)
* SSL cert/key
  * docker/nginx/ssl/server.cert
  * docker/nginx/ssl/server.key
  * can generate self signed certificate/key from www.selfsignedcertificate.com for dev environment


# Setting up a new league

* log in at https://gmtarr-api.rrish.org/admin/
* find event number at https://gmtarr-api.rrish.org/api/events
* create league https://gmtarr-api.rrish.org/api/events/{event_id}/create-league
* change name of league (add year prefix, etc.) https://gmtarr-api.rrish.org/admin/api/flight/
* go to admin and filter players by league, gender, level...
* figure out how many flights are needed at each gender/level and create them https://gmtarr-api.rrish.org/admin/api/flight/
  * no more than 10 players per flight
  * if only 2 or 3 players registered for a particular gender/level, consider combining with an adjacent level
* go back to (filtered) players list, select players you want to add to a flight, and use "Bulk Set Flight" action to assign them to a flight
  * can consider previous flight standings if you need to pick a few players to "promote" up to the next level to make it viable
  * when dividing players into flights, it usually works pretty well to sort by name and then just select every Nth player, where N is the number of flights for that level
* generate schedule for each flight https://gmtarr-api.rrish.org/api/flights/{flight_id}/generate-schedule
  * if small flight, consider generating a second round
    * after generating first round, go and edit the Flight's start date and then go back and hit the `generate-schedule` api endpoint again
    * then change start date back to the original start date
* export registrants from Wild Apricot's Event admin
* go to Audience Dashboard and select Import Contacts
* updload the exported CSV
* import to "Current Members", Subscribed
  * make sure to check the box for UPDATE EXISTING or else the new tag won't get applied to existing contacts
* add a tag for the round robin, e.g. `rr-2022-fall`
* make sure first name, last name, and email fields are properly mapped
* replicate a previous version of "Round Robin Schedule Released" campaign, edit, and send to the contacts tagged with the new tag from above
