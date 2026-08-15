export const PROGRAMMING_LANGUAGES = [
  {
    id: "cpp",
    name: "C++",
    monacoLanguage: "cpp",
    extension: ".cpp",
    starterCode: `#include <iostream>
using namespace std;

int main() {

    return 0;
}`,
  },

  {
    id: "python",
    name: "Python",
    monacoLanguage: "python",
    extension: ".py",
    starterCode: `def main():
    pass


if __name__ == "__main__":
    main()`,
  },

  {
    id: "java",
    name: "Java",
    monacoLanguage: "java",
    extension: ".java",
    starterCode: `public class Main {

    public static void main(String[] args) {

    }

}`,
  },

  {
    id: "javascript",
    name: "JavaScript",
    monacoLanguage: "javascript",
    extension: ".js",
    starterCode: `function main() {

}

main();`,
  },
  {
  id: "c",
  name: "C",
  monacoLanguage: "c",
  extension: ".c",
  starterCode: `#include <stdio.h>

int main() {

    return 0;
}`,
},
{
  id: "verilog",
  name: "Verilog",
  monacoLanguage: "verilog",
  extension: ".v",
  starterCode: `module main;

initial begin

end

endmodule`,
},
{
  id: "sql",
  name: "SQL",
  monacoLanguage: "sql",
  extension: ".sql",
  starterCode: `CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    salary INTEGER
);

INSERT INTO employees (id, name, salary) VALUES
    (1, 'Alice', 90000),
    (2, 'Bob', 75000);

SELECT * FROM employees;`,
},
];

export const DEFAULT_LANGUAGE = PROGRAMMING_LANGUAGES[0];