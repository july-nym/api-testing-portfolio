# java-rest-assured

API test suite built with **Java 17 + REST Assured + TestNG + Maven**.

## Highlights
- Fluent **Given/When/Then** REST Assured syntax
- **POJO (de)serialization** with Jackson + Lombok (`User`, `Booking`)
  — including snake_case → camelCase mapping via `@JsonProperty`
- JSON schema validation (`json-schema-validator` module)
- TestNG **groups** (`smoke`, `regression`, `negative`) + data providers
- **Allure** reporting (AspectJ-woven `@Step`/`@Description`)
- **Maven profiles** for environment selection (`dev`, `staging`, `smoke`)

## Run it
```bash
mvn test                          # full suite, dev profile
mvn test -Psmoke                  # smoke group only
mvn test -Pstaging -Denv=staging  # staging config

# Allure report (after a run)
mvn test && allure serve target/allure-results
```

Config defaults live in `src/test/resources/config-dev.properties`; the
`REQRES_BASE_URL` / `REQRES_API_KEY` / `BOOKER_BASE_URL` env vars override them
at runtime so CI never edits a checked-in file.

## Layout
```
src/test/java/io/portfolio/qa/
  base/BaseTest.java          spec setup + cached booker token
  models/User.java            Lombok + Jackson POJOs
  models/Booking.java
  utils/ApiClient.java        request specs, config loading
  utils/SchemaValidator.java  classpath schema matcher
  tests/                      Auth / User / Booking / Negative
src/test/resources/
  schemas/                    JSON schemas
  config-*.properties         per-env config
testng.xml / testng-smoke.xml suite definitions
```
