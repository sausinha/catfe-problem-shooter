import os
import zipfile

# Define project directory and zip file path
project_root = "/mnt/data/context-aware-testing"
zip_file_path = "/mnt/data/context-aware-testing.zip"

# Create project directory structure
os.makedirs(f"{project_root}/src/main/java/com/example/testing/controller", exist_ok=True)
os.makedirs(f"{project_root}/src/main/java/com/example/testing/service", exist_ok=True)
os.makedirs(f"{project_root}/src/main/java/com/example/testing/repository", exist_ok=True)
os.makedirs(f"{project_root}/src/main/java/com/example/testing/entity", exist_ok=True)
os.makedirs(f"{project_root}/src/main/java/com/example/testing/config", exist_ok=True)
os.makedirs(f"{project_root}/src/test/java/com/example/testing", exist_ok=True)

# Sample Java files to include in the project
java_files = {
    "controller/TestCaseController.java": '''
package com.example.testing.controller;

import com.example.testing.entity.TestCase;
import com.example.testing.service.TestCaseService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/test-cases")
@RequiredArgsConstructor
public class TestCaseController {
    private final TestCaseService testCaseService;

    @GetMapping
    public List<TestCase> getAllTestCases() {
        return testCaseService.getAllTestCases();
    }

    @PostMapping
    public TestCase createTestCase(@RequestBody TestCase testCase) {
        return testCaseService.createTestCase(testCase);
    }
}
''',

    "service/TestCaseService.java": '''
package com.example.testing.service;

import com.example.testing.entity.TestCase;
import com.example.testing.repository.TestCaseRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class TestCaseService {
    private final TestCaseRepository testCaseRepository;

    public List<TestCase> getAllTestCases() {
        return testCaseRepository.findAll();
    }

    public TestCase createTestCase(TestCase testCase) {
        return testCaseRepository.save(testCase);
    }
}
''',

    "repository/TestCaseRepository.java": '''
package com.example.testing.repository;

import com.example.testing.entity.TestCase;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TestCaseRepository extends JpaRepository<TestCase, Long> {
}
''',

    "entity/TestCase.java": '''
package com.example.testing.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "test_cases")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TestCase {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String scenario;
    private String expectedResult;
    private String status;
}
''',

    "config/OpenAPIConfig.java": '''
package com.example.testing.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenAPIConfig {
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info().title("Context-Aware Testing API")
                        .version("1.0")
                        .description("API for automated AI-driven test case generation"));
    }
}
'''
}

# Write Java files to the project structure
for file_path, content in java_files.items():
    full_path = os.path.join(project_root, "src/main/java/com/example/testing", file_path)
    with open(full_path, "w") as file:
        file.write(content)

# Create a zip file of the project
with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(project_root):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, project_root))

# Return the zip file path
zip_file_path