package io.portfolio.qa.utils;

import io.restassured.builder.RequestSpecBuilder;
import io.restassured.http.ContentType;
import io.restassured.specification.RequestSpecification;

import java.io.InputStream;
import java.util.Properties;

/**
 * Builds reusable REST Assured request specs, one per target API.
 *
 * Centralising the specs keeps base URLs out of the test bodies, so a test reads
 * as pure Given/When/Then. Config is loaded from
 * config-${env}.properties, selected by the `env` system property (wired through
 * a Maven profile), falling back to dev.
 */
public final class ApiClient {

    private static final Properties CONFIG = load();

    private ApiClient() {
        // static factory only
    }

    private static Properties load() {
        String env = System.getProperty("env", "dev");
        String resource = "config-" + env + ".properties";
        Properties props = new Properties();
        try (InputStream in = ApiClient.class.getClassLoader().getResourceAsStream(resource)) {
            if (in == null) {
                throw new IllegalStateException("Missing config resource: " + resource);
            }
            props.load(in);
        } catch (Exception e) {
            throw new IllegalStateException("Could not load " + resource, e);
        }
        // env vars win over the file so CI can override without editing resources
        overrideFromEnv(props, "JSONPLACEHOLDER_BASE_URL", "jsonplaceholder.baseUrl");
        overrideFromEnv(props, "BOOKER_BASE_URL", "booker.baseUrl");
        return props;
    }

    private static void overrideFromEnv(Properties props, String envKey, String propKey) {
        String value = System.getenv(envKey);
        if (value != null && !value.isBlank()) {
            props.setProperty(propKey, value);
        }
    }

    public static String get(String key) {
        return CONFIG.getProperty(key);
    }

    public static long maxResponseMs() {
        return Long.parseLong(CONFIG.getProperty("maxResponseMs", "2000"));
    }

    /** jsonplaceholder spec — keyless, used for user reads + post CRUD. */
    public static RequestSpecification jsonplaceholder() {
        return new RequestSpecBuilder()
                .setBaseUri(CONFIG.getProperty("jsonplaceholder.baseUrl"))
                .setContentType(ContentType.JSON)
                .setAccept(ContentType.JSON)
                .build();
    }

    public static RequestSpecification booker() {
        // NOTE: use an explicit "application/json" Accept rather than
        // setAccept(ContentType.JSON). REST Assured expands ContentType.JSON into
        // a multi-value Accept ("application/json, application/javascript, …"),
        // and restful-booker answers that with a 418. A clean single value is fine.
        return new RequestSpecBuilder()
                .setBaseUri(CONFIG.getProperty("booker.baseUrl"))
                .setContentType(ContentType.JSON)
                .addHeader("Accept", "application/json")
                .build();
    }
}
