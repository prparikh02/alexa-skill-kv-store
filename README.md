# alexa-skill-kv-store
Key-Value store for Alexa so you can save your arbitrary key-value pairs.

## Background

A long time ago I thought it would be cool if Alexa could save abitrary tidbits of information like remembering that you parked your car in spot number 14 (`{"key": "my parking spot", "value": 14}`)or that your desk height is 42 inches (`{"key": "desk height", "value": "42 inches"}`). Turns out as of May 2018 this is now possible (https://amzn.to/2SlMpTu). Looks like I was too late to the party.

So fast forward March 2019 and I am using this small skill as an opportunity to learn more about AWS CodePipeline, CodeDeploy, and CodeBuild. For example, commits to this repo's `master` branch will kick off CodePipeline, which will then build according to the SAM buildspec and template files, and then deploy to Lambda, and much more AWS magic in between. I also got to refresh my memory on `boto3`, `DynamoDB`, and `Lambda`.

Currently, this repo is largely two weekends of work, the first being researching AWS resources with which I was unfamiliar, and the second actually working with the Alexa Skill code. I learned a great deal so it was not for naught.

### [TODO] - Update with which resources I used for AWS CodePipeline set up

Eventually... here's [this AWS doc](https://docs.aws.amazon.com/lambda/latest/dg/build-pipeline.html) for now.
