CI

is a  small FastAPI app with a complete CI/CD pipeline. Every push to `main` is tested, packaged as a Docker image, and published to Docker Hub.

## Pipeline


git push --> {pytest} --> {dockerbuild} --> {push to dockerhub} --> deploy in a cloud provider
                |-->if anything fail nothing is moved to deployment

why dockerhub --> the ci/cd only build on a runner which is a temporary machine and deleteed when the process is over. Therefore the ci/cd build and push images in a permanent place where it is always online. Through this the online providers can know acces the docker images in docker hub

# what is used:
fastapi
docker
Github Actions
Docker Hub
Pytest


## Endpoints

| Route | Response |
|---|---|
| `/` | `{"message": "Hello from CI/CD", "version": "1.0"}` |
| `/health` | `{"status": "ok"}` |

## Run it

With Docker:

```bash
docker run -d -p 8000:8000 brianlomunyak/hello-cicd:latest
```

Without Docker:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Run the tests:

```bash
pytest -v
```

## Design decisions

- **Tests gate the build.** `build-and-push` uses `needs: test`, so a failing test means no image is published.
- **Builds only on push to `main`.** Pull requests run tests but never publish.
- **Two image tags.** `latest` for convenience, and the commit SHA so every image traces back to exact code and can be rolled back.
- **Secrets in GitHub Secrets.** Docker Hub credentials are never stored in the repo.
- **Docker Hub access token, not my password.** The token has Read & Write scope only and can be revoked without touching my account.
- **Dependency layer cached.** `requirements.txt` is copied before the code, so code edits rebuild in seconds.

## Problems I hit and how I fixed them

| Failure | Cause | Fix |
|---|---|---|
| `collected 0 items`, exit code 5 | `test_main.py` was never committed | Added the file to git, checked with `git ls-files` |
| Container `Exited (3)` | Dockerfile `CMD` used `main.py` instead of `main:app` | Corrected the uvicorn target |
| `Username and password required` | Workflow secret names didn't match the ones saved in GitHub | Matched the names in `ci.yml` |
| `unauthorized: incorrect username or password` | Wrong Docker Hub username and an outdated token | Used the real Docker ID and tested with `docker login` first |
| `401 ... insufficient scopes` on build | Token had the Cloud Sandboxes scope instead of Repo Read & Write | Generated a new token with the right scope |

## Roadmap

- [ ] Deploy to AWS EC2
- [ ] Auto-deploy from the pipeline over SSH
- [ ] Provision the server with Terraform