# An MLOps Workflow using Cloudera Machine Learning and Cloudera Data Engineering

Machine learning (ML) plays a critical role in optimizing the
value of digital transformation. Across industries, organizations seek to leverage the digital revolution for more
revenue or lower costs.

However, it’s not as easy as it may seem to effectively deploy
machine learning in the enterprise.


The overall objective should
be to quickly and seamlessly be able to move ML models and
operate increasing numbers of models on a continuous basis. This
is hard, and in this book you find out about the right production
machine learning approaches, best practices, and MLOps technology that is critical for creating, sustaining, and scaling your
business impact using ML.

To succeed with your ML investment, you need to rapidly implement and scale ML models across your entire organization. Usually these implementation scenarios span a large spectrum of ML
use cases. The need for organizational speed in combination with
growing regulatory scrutiny related to data and AI/ML, create new
and unique challenges to move ML models from idea and experimentation, to production.

Currently only 35 percent of organizations indicate that
their ML models are fully and successfully deployed in production. And on top of that, the journey doesn’t end when models are
deployed. On the contrary, it’s vital to ensure that models continue to operate and perform as expected, or even better and more
optimized, throughout their entire lifecycle.

A typical data science workflow goes through different phases but
is complex and highly iterative. At the bottom of Figure 1-1 you
can see the various steps of a data science workflow from data to
models to outcomes to business value. The figure itself is mapped
into three main phases: data engineering, data science, and production. This figure also has slightly more emphasis on the production
phase and the governance aspects than a typical ML workflow.

![alt text](images/ml-lifecycle-mlopsfordummies.png)

However, for enterprises, even before the data engineering workflow is started, it’s vital to secure that you have a robust data
management and IT practice in place to ensure enterprise governance, security, access control, and data lineage. This is a key
part of the ML lifecycle because it eliminates things like silos and
creates an observable, explainable, and transparent foundation
for the execution of the ML workflow.

![alt text](images/ml-lifecycle-governance-full.png)


## Data engineering

This phase consists of tasks such as data acquisition, processing,
and governance. In this context data processing refers to transforming raw data by cleansing and preparing datasets to a more
convenient format for a developer or a data engineer to run an
analysis on.
As organizations use data (and analytics) more, and for more
important questions and user scenarios, the need be able to rely on
the data, and therefore the need to govern those assets, increases.
Every organization should be concerned about data quality in
their source systems, but often these concerns are isolated and
not visible across departments. Security, privacy, and regulatory
compliance are also important elements of data governance.


## Data science

Data science is an interdisciplinary field that uses scientific methods, processes, algorithms, and systems to extract knowledge and
insights from structured and unstructured data. Data science is
also a concept to unify statistics, data analysis, machine learning, and other related methods to understand and analyze actual
phenomena with data spanning from more traditional business
intelligence (BI), through analytics, and more exploratory ML
techniques.

More traditional analytics and BI includes areas such as data
preparation, data visualization, and data modeling. Data preparation refers to the process of transforming and mapping data from
its raw data form into another format with the intent of making it
more appropriate and valuable for a variety of analytics use cases.
Data visualization (or data exploration as it´s also called) on the
other hand helps identify interesting patterns and trends in the
data that can be identified and analyzed through simple charts 

such as line charts or bar charts. Data modeling is the process of
producing a descriptive diagram of relationships between various
types of information that are stored in a database.
Exploratory data science and ML includes probabilistic modeling
and ML model development (model training and testing), where
probabilistic modeling helps understand the probability of what
could happen based on a variety of inputs and data.
ML model development can also be focused on automating processes or making ongoing predictions that learn/change based
on new data. ML model development can be targeting a certain product, such as learning what a person regularly watches
on Netflix and suggesting programming they will likely enjoy.
Another objective can be a business segment, for example security
and fraud prevention, where the ML model shall detect anomalies or patterns in incoming data to enable proactive detection of
breaches.


## Production

This part of the ML lifecycle is focused on the process of delivering the outcomes (better automation, predictions, innovations)
to stakeholders (customers, internal business). There are several different ways to deploy a model and it´s key to understand
the end user (customer) objective to determine the technology
required.
What the deployment phase actually means can differ a lot depending on what type of use case you’re trying to realize. It could be
as simple as generating a report, or as complex as implementing a repeatable data science process critical for business operations. Regardless of use case, however, successful production ML
requires a streamlined, frictionless and predictable deployment,
and ongoing governance of ML models in production, at scale.


## Identifying Challenges with Getting ML to Production

Deploying and scaling AI/ML across the enterprise requires
implementing complex, iterative workflows end-to-end from
capturing data through developing ML models to achieving the
expected outcomes. This is not an easy task. In addition, as the
number of AI/ML projects and models multiply, production ML
can be slow, cumbersome, and fraught with “false starts” that
make it even more difficult and expensive.
While the end-to-end ML lifecycle has always been pitched as an
actual “cycle,” to date there has been limited success in actually
managing this end-to-end process at enterprise level scale. Some
reasons for this are:

* Data scientists are usually not trained engineers and thus
don’t always follow good DevOps practices.
* Data engineers, data scientists, and the engineers responsible for delivery operate in silos that creates friction between
teams.
* The myriad of machine learning tools and frameworks
fosters a lack of standardization across the industry.

Machine learning realization from an enterprise perspective is
slow and tough to scale. There is not much automated, collaboration is difficult, and the actual operationalized models delivering
business value are few.
Many projects don’t make it into production because of model
inefficiencies that slow down or halt the entire process. Or, in
many cases, organizations fail to adequately adopt production
models because of a lack of internal knowledge on how they work
and other cultural/business impediments.
As organizations start to see artificial intelligence (AI) and
machine learning (ML) as fundamental and vital pieces of the
company, organizations are usually wrestling with growing organizational pain. Isolated projects exist in silos across the enterprise, putting quality, security, governance, and compliance at
risk. When applying an “AI factory” approach to turning data
into decisions, you can make the process of building, scaling, and
deploying enterprise ML solutions automated, repeatable, and
predictable, but lose the business value along the way.
Only through the industrialization of AI can you shift focus from
technology solutions to business outcomes, empower continuous optimization, and encourage a learning culture across the
enterprise.

Truly excellent industrial-grade ML requires transformation in
almost every part of an organization, and as a result, production
ML hurdles are often actually organization wide hurdles. Some of
these hurdles are described in the following sections.


## Unsatisfactory model monitoring

Efficient monitoring of models in operation is an essential element of production deployment as it provides visibility into its
various phases. Poor visibility into mathematical metrics and to
the external tools used for monitoring is a major challenge. Custom tooling to monitor the technical health of models doesn’t
scale and mathematical monitoring is hard, customized, and little
to no tooling exists.
On the other hand, standard monitoring tools tend to be too
generic for identifying model drift, such as identifying whether
the ML model execution is deviating from its objective. The truth
is that what really happened based on the prediction is usually
only understood well after the fact. This means that determining
whether a model is functioning as it should needs to be customized on a per model basis.


## Inefficient deployment

Data scientists today use a variety of different tools to solve many
critical business problems. This often results in models being
recoded into different languages as the initial language may not
be used in the production environment. This leads to longer cycle
times and potential inconsistencies in the translated model.


## Inadequate ML governance

As AI/ML moves to production, the need to govern all IT assets
(data, models, infrastructure, for example) and ensure security,
privacy, and regulatory compliance increases. Defining standards
for ML Operations (MLOps) is essential for deploying and governing ML models at scale for enterprises. This includes visibility of
models within teams and across organizations. It enables teams
to understand how ML is being applied in their organizations and
requires an official catalog of models.

In the absence of such a model catalog, many organizations
are unaware of their models and features, such as where they
are deployed and what they are doing. This leads to substantial
rework, model inconsistency, recomputing features, and other
inefficiencies.


## Insufficient security measures

There is a need for end-to-end enterprise security from data to
the production environment. The chosen platform must be capable of delivering models into production with inherited security,
unified authorization, and access tracking.


## Inability to scale

As the model moves forward to production, it’s typically exposed
to larger volumes of data. The platform must have the ability to
scale from small to large volumes of data and automate model
creation. Applied machine learning at enterprise scale requires a
particular combination of cutting-edge technology and enterprise
expectations.
Additionally, it’s not only about scale of data, but the number
of actual models in production. Operating and monitoring a few
models may be fine, but when you scale up to hundreds of models it’s very difficult to make sure they are not drifting and are
maintaining their reliability. This is a common concern for customers in the banking sector, where they have entire teams of ML
engineers dedicated to just keeping their models accurate in the
long term.

A major concern is also when brand new (and at times) untested
or poorly supported technology, tools, and systems are rapidly
deployed into enterprise application workflows aimed for the ML
lifecycle and are expected to perform at least as well as existing
software that has been in place (at times) for years.


# Detailing Key Capabilities of Production ML

Production ML capabilities include:
» Packaging, deployment, and serving are the three first
steps in production ML. Right packaging is necessary for
automated deployment of production models and to
address multiple deployment patterns. Enterprise level
deployments need high availability, autoscaling, and strong
authentication features. Serving makes a trained model
available to other software components. Models can be
served in batch or real-time modes.
» Monitoring is an important element of operationalizing
ML. After a model is deployed into production and providing
utility to the business, it’s necessary to monitor how well
the model is performing. There are several aspects of
performance to consider, and each has its own metrics and
measurements that impacts the lifecycle of the model.
However, monitoring is done at various stages of the lifecycle,
for example to check input and output distribution, look for
skew, model drift and accuracy change, add custom
thresholds, send emails with results, and trigger alarms.
» Model governance, cataloging, and lineage tracking are a
basic requirement for model governance and enable teams
to understand how ML is being applied in their organizations.
Governance requires a centralized catalog of models and
features that facilitate tracking models and their features
throughout their lifecycle to understand these features and
their relationship with the data catalog. Catalogs also facilitate
authorization and tracking access to models thereby maintaining end-to-end security of the environment.
Data lineage regards the need to have visibility into the full
ML lifecycle, starting with where the data originates and
ending with the ongoing production environment. This
includes every process along the way, from data ingest to
data engineering, to model building, deployment, serving,
and production, and even security and governance
visibility — who touched what when, what data powered
what models, and who had access to this data at every step.

![alt text](images/ml-lifecycle-prod-workflow.png)

So, what does good MLOps look like? How can you ensure that
you’re getting your production ML right from start? Well, good
MLOps looks a lot similar to good DevOps.
» Reduce the time and difficulty to push models into
production.
» Decrease friction between teams and enhance collaboration.
» Improve model tracking, versioning, monitoring, and
management.
» Create a truly cyclical lifecycle for the modern ML model.
» Standardize the machine learning process to prepare for
increasing regulation and policy.

![alt text](images/ml-lifecycle-iterative-sport.png)

As opposed to ML point solutions, a unified data platform doesn’t compromise security or require complex, costly workflows for
production models. Instead you get an end-to-end ML platform
that enables standards-driven model and feature monitoring,
cataloging, and ongoing governance at enterprise scale.


## Describing the Cloudera Data Platform

Cloudera Data Platform (CDP) is an enterprise data cloud, which
functions as a platform for both IT and the business. It incorporates support for an environment running both on on-premises
and in a public cloud setup. CDP also has multi-cloud and multifunction capabilities at the same time as it’s both simple to use
and secure by design. It supports both manual and automated
functions and is open and extensible. It offers a common environment for both data engineers and data scientists, supporting
data science team collaboration. Figure  4-2 shows a capability
overview of CDP.
The data platform from Cloudera provides self-service access to
integrated, multi-function analytics on centrally managed and
secured business data while deploying a consistent experience
anywhere  — on-premises or in hybrid and multi-cloud. This
includes consistent data security, governance, lineage, and control, while deploying the efficient, easy-to-use cloud analytics,
eliminating end-user need for shadow IT solutions.

To optimize the data lifecycle CDP has multi-function analytics
capabilities that integrate data management and analytic experiences across the data lifecycle. You can collect, enrich, report,
serve, and model enterprise data for any business use case in any
cloud.
Because high value, data-driven business use cases require modern, streaming real-time data, CDP has integrated analytics and
machine learning services that are both easy for IT to manage and
deploy and easy for business users to consume and operationalize.
CDP makes it easy to deploy modern, self-service analytics and
machine learning services for any data, with shared security and
governance and the flexibility to scale with the same experience.
CDP also delivers security, compliance, migration, and metadata
management across all environments.
CDP is an open platform where you can add and build your solutions using open source components including open integrations.
It’s also open to multiple data stores and compute architectures.
This in turn
enables the following capabilities:

* A holistic view of data and metadata.
* A common data catalog across all your deployments
worldwide in various data centers and clouds.
* Synchronization of data sets and metadata policies between
infrastructures as needed.
* Bursting on-premises workloads into the cloud when more
capacity is needed.
* Analyzing and optimizing workloads regardless of where the
workloads run.

![alt text](images/ml-lifecycle-datamgt.png)

On top of the data platform you can run Cloudera Machine Learning
(CML); refer to Figure 4-1. CML has extensive MLOps features and
a set of model and lifecycle management capabilities to enable 
the repeatable, transparent, and governed approaches necessary
for scaling model deployments and ML use cases. It´s built to support open source standards and is fully integrated with Cloudera
Data Platform, enabling customers to integrate into existing and
future tooling while not being locked into a single vendor.
Cloudera Machine Learning (CML) enables enterprises to proactively monitor technical metrics such as service level agreements
(SLA) adherence, uptime, and resource use as well as prediction
metrics including model distribution, drift, and skew from a single governance interface. Users can set custom alerts and eliminate the model “black box” effect with native tools for visualizing
model lineage, performance, and trends.
Some of the benefits with CML include:

* Model cataloging and lineage capabilities to allow visibility
into the entire ML lifecycle, which eliminates silos and blind
spots for full lifecycle transparency, explainability, and
accountability.
* Full end-to-end machine learning lifecycle management that
includes everything required to securely deploy machine
learning models to production, ensure accuracy, and scale
use cases.
* An extensive model monitoring service designed to track and
monitor both technical aspects and accuracy of predictions
in a repeatable, secure, and scalable way.
* New MLOps features for monitoring the functional and
business performance of machine learning models such as
detecting model performance and drift over time with native
storage and access to custom and arbitrary model metrics;
measuring and tracking individual prediction accuracy,
ensuring models are compliant and performing optimally.
* The ability to track, manage, and understand large numbers
of ML models deployed across the enterprise with model
cataloging, full lifecycle lineage, and custom metadata in
Apache Atlas.
* The ability to view the lineage of data tied to the models built
and deployed in a single system to help manage and govern
the ML lifecycle.
* Increased model security for Model REST endpoints, which
allows models to be served in a CML production environment without compromising security.

Furthermore, all enterprise production ML workflows are
securely contained in CDP, Cloudera’s enterprise data cloud. This
enables seamless workflows for governing and quickly customizing models in production while maintaining complete visibility
into the end-to-end data and model lineage. Clients can effectively maintain hundreds or thousands of models in production
with resources that auto-scale to business needs and set model
governance rules that enable fast response to mission critical
changes in their production environments.
Governing production ML workflows in CML enables enterprises
to accelerate time to value and deliver ongoing results securely.
CML is able to integrate data management with explainable,
interoperable, and reproducible MLOps workflows in various execution environments, from edge to cloud.

![alt text](images/ml-lifecycle-fordummiesscreenshot.png)

To learn more about Enterprise Machine Learning, MLOps and the Cloudera Data Platform please [download the full book](https://www.cloudera.com/campaign/production-machine-learning-for-dummies.html) authored by Santiago Giraldo Anduaga, Product Marketing Director at Cloudera. 



## Demo Instructions

WIP

