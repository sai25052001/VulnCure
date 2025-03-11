package com.example;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class VulnerableClass {
    private static final Logger logger = LogManager.getLogger(VulnerableClass.class);

    public static void main(String[] args) {
        logger.info("This application might be vulnerable to Log4j exploits.");
    }
}

