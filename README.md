# FlixPicks-Front

## Launching Application
> [!CAUTION]
> The website requires a running instance of the database to function.
> Follow the below instructions to ensure successful startup.

### Local Development
1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) on your computer and ensure it's running.
2. Create a directory on your PC to hold all the required repos.
3. Clone each requried repo below (Folders should be named exactly as shown)
    - Docker-Compose
    - FlixPicks-Front
    - FlixPicks-DB
4. Copy and paste the 'docker-compose.yml' file into the top-level directory.
5. Use the commands below to build, launch, or stop docker containers.


### Docker Commands

#### Build Images
> docker-compose build

#### Start Services (Containers and Network)
> docker-compose up
Note: Add -d to run detached (i.e. background)

#### Shutdown Services
> docker-compose down
NOTE: Use the clean-up method below, otherwise you will need to manually clean-up containers.

#### Remove and Clean-up Containers/Images
> docker-compose down --rmi all -v --remove-orphans


### Remoate Development (FlixPicks VM)
1. Connect to the ODU CS VPN
2. Launch the VM using the following ssh command (add your cs_username)
    > ssh -A -Y cs_username@cs411-orang.student.cs.odu.edu
3. Follow the steps 2 thru 5 from Local Development (No real difference other than Docker is already installed)
4. Once the containers are running, go to the web address: cs411-orang.student.cs.odu.edu


## Example Data:
There is currently one test user setup, use the credentials below to try it out.
Username: test
Password: 12345


## Sources used:
[Python Login Tutorial](https://www.youtube.com/watch?v=71EU8gnZqZQ)