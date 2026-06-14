package io.portfolio.qa.utils;

import io.restassured.builder.RequestSpecBuilder;
import io.restassured.http.ContentType;
import io.restassured.specification.RequestSpecification;

import java.io.InputStream;
import java.util.Properties;

/**
 * Builds reusable REST Assured request specs, one per target API.
 *
 * Centralising the specs keeps base URLs and the reqres API key out of the test
 * bodies, so a test reads as pure Given/When/Then. Config is loaded from
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
        overrideFromEnv(props, "REQRES_BASE_URL", "reqres.baseUrl");
        overrideFromEnv(props, "REQRES_API_KEY", "reqres.apiKey");
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

    /** reqres spec, pre-loaded with the API key it now requires for writes. */
    public static RequestSpecification reqres() {
        return new RequestSpecBuilder()
                .setBaseUri(CONFIG.getProperty("reqres.baseUrl"))
                .addHeader("x-api-key", CONFIG.getProperty("reqres.apiKey"))
                .setContentType(ContentType.JSON)
                .setAccept(ContentType.JSON)
                .build();
    }

    public static RequestSpecification booker() {
        return new RequestSpecBuilder()
                .setBaseUri(CONFIG.getProperty("booker.baseUrl"))
                .setContentType(ContentType.JSON)
                .setAccept(ContentType.JSON)
                .build();
    }
}
