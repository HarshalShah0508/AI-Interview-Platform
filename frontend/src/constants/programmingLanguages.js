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
];

export const DEFAULT_LANGUAGE = PROGRAMMING_LANGUAGES[0];