#### Architecture Design Options
- psql db with pregenerated pairs
- pairs in random order in db
- backend scans for a row with open `status` enum to present to the user
  - `status` should be updated to prevent overwriting by multiple users
- cron job to scan the db and apply rules engine
- cron job to look for expired open rows
#### commands
`docker run --rm -d -p 8080:80 dpage/pgadmin4`
`docker run --rm --name pdb -e POSTGRES_PASSWORD=p -p 5432:5432 -d postgres`
`docker run --rm -it postgres psql -h $(grep server /etc/hosts | awk '{print $1}') -U postgres`