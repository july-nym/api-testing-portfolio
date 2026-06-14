package io.portfolio.qa.utils;

import io.restassured.module.jsv.JsonSchemaValidator;
import org.hamcrest.Matcher;

/**
 * Tiny convenience layer over REST Assured's JsonSchemaValidator so tests write
 *   .body(SchemaValidator.matchesSchema("single-user.json"))
 * instead of repeating the classpath matcher form everywhere. Schemas live in
 * src/test/resources/schemas/.
 */
public final class SchemaValidator {

    private SchemaValidator() {
    }

    public static Matcher<?> matchesSchema(String schemaFileName) {
        return JsonSchemaValidator.matchesJsonSchemaInClasspath("schemas/" + schemaFileName);
    }
}
