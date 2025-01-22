# include .env.stage

CONTAINER_NAME=business_service
REPO=192.168.222.108:8082
TAG=$(APP_VERSION)

fresh:  ## Destroy & recreate all uing dev containers.
	make stop destroy build start

fresh-stage: ## Destroy & recreate all using prod containers.
	make stop-stage destroy-stage build-stage start-stage

fresh-prod: ## Destroy & recreate all using prod containers.
	make stop-prod destroy-prod build-prod


stage-update: tag-stage start-stage

pro-update: tag-pro push-pro start-pro

clr-stage: #kkffsdf
	@docker rm -f ${CONTAINER_NAME}
	@docker rmi -f ${REPO}/${CONTAINER_NAME}:staging

clr-img: #kkffsdf
	@docker rmi -f $(docker images '${REPO}/${CONTAINER_NAME}' -q)


###########============Local Dev========================

build: ## Build all containers
	@docker build --no-cache . -f ./Dockerfile
start: ## Start all containers
	@docker-compose -f docker-compose.yml up --force-recreate -d
stop: ## Stop all containers
	@docker-compose -f docker-compose.yml stop
restart: stop start ## Restart all containers
destroy: stop ## Destroy all containers

####================== Build staging evironment ====================================
build-stage:## Build all containers for DEV
	@docker build . --no-cache -t ${CONTAINER_NAME} -f ./Dockerfile-staging

start-stage: ## Start all containers
	@docker-compose -f docker-compose-stage.yml up --force-recreate -d
stop-stage: ## Stop all containers
	@docker-compose  -f docker-compose-stage.yml stop
restart-stage: stop-stage start-stage ## Restart all containers
destroy-stage: stop-stage ## Destroy all containers

tag-stage:
	@docker tag ${CONTAINER_NAME} ${REPO}/${CONTAINER_NAME}:${TAG}
	@docker tag ${CONTAINER_NAME} ${REPO}/${CONTAINER_NAME}:staging
push-stage:
	@docker push ${REPO}/${CONTAINER_NAME}:${TAG}
	@docker push ${REPO}/${CONTAINER_NAME}:staging


####================== Build Production evironment ====================================
build-pro:## Build all containers for DEV
	@docker build . -f ./Dockerfile-pro \
    --build-arg app_env='production' \
    --build-arg app_url='https://core-api.gdi.gov.kh' \
    --no-cache -t ${CONTAINER_NAME}

start-pro: ## Start all containers
	@docker-compose -f docker-compose-pro.yml up --force-recreate -d
stop-pro: ## Stop all containers
	@docker-compose -f docker-compose-pro.yml stop
restart-pro: stop-pro start-pro ## Restart all containers
destroy-pro: stop-pro ## Destroy all containers


tag-pro:
	@docker tag ${CONTAINER_NAME} ${REPO}/${CONTAINER_NAME}:${TAG}
	@docker tag ${CONTAINER_NAME} ${REPO}/${CONTAINER_NAME}:pro
push-pro:
	@docker push ${REPO}/${CONTAINER_NAME}:${TAG}
	@docker push ${REPO}/${CONTAINER_NAME}:pro


# docker build . -f ./Dockerfile-staging --build-arg app_env='stage' --build-arg db_host='192.168.222.110' --build-arg db_database='stage_invoice_db' --build-arg db_username=sophea --build-arg db_password=S0phea@mis  --no-cache -t gdi_billing
# make tag-stage start-stage
