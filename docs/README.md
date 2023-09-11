# Aura CLI Documentation

This folder contains the documentation for the Aura CLI project. The pages are written in AsciiDoc, and generated into webpages by Antora.

An external workflow picks up this directory, embeds it into the Neo4j docs, and makes sure generated files are automatically deployed to:

```
https://neo4j.com/labs/aura-cli/{version}
```

For example: https://neo4j.com/labs/aura-cli/1

## Local Build

To compile and view the documentation locally, navigate to this (`./docs`) folder and run:

```
yarn install
yarn start
```

Then, open your browser and navigate to http://localhost:8000/.
