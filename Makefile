help: ## Show help
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install for Cloud9
	@sudo yum install -y jq

.PHONY: clean
clean: ## Remove unused images
	@docker system prune -f
	@docker volume prune -f
	@docker image prune -f

.PHONY: run
run: ## Build and Run
	@docker build -t ${REPOSITORY_NAME} .
	@docker run --rm -p 9000:8080 ${REPOSITORY_NAME}

.PHONY: test
test: ## Test
	@curl -sd '{}' http://localhost:9000/2015-03-31/functions/function/invocations | jq .

.PHONY: login
login: ## Login to ECR
	@aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin ${REGISTRY_URL}

.PHONY: push
push: ## Push images
	@docker tag ${REPOSITORY_NAME} ${REGISTRY_URL}/${REPOSITORY_NAME}
	@docker push ${REGISTRY_URL}/${REPOSITORY_NAME}
