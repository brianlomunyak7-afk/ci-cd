# CI

is a  small FastAPI app with a complete CI/CD pipeline. Every push to main is tested, packaged as a Docker image, and published to Docker Hub.

## Pipeline


git push --> {pytest} --> {dockerbuild} --> {push to dockerhub} --> deploy in a cloud provider
                |-->if anything fail nothing is moves forward

why dockerhub --> the ci/cd only build on a runner which is a temporary machine and deleteed when the process is over. Therefore the ci/cd build and push images in a permanent place where it is always online. Through this the online providers can know acces the docker images in docker hub

# what i used:
fastapi --> is the app
Docker --> packages it
Github Actions --> automate the build
Docker Hub --> store the docker images so servers can pull it
Pytest --> test the app

# Runnning it locally

using git:
 ```bash
 git clone https:github.com/brianlomunyak7-afk/ci.git

 cd ci

 using vs code:
  cd ci: code .

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


