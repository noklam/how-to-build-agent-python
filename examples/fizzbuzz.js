// FizzBuzz implementation in JavaScript
// Prints numbers 1-100, replacing multiples of 3 with "Fizz",
// multiples of 5 with "Buzz", and multiples of both with "FizzBuzz"

function fizzbuzz(limit = 100) {
    for (let i = 1; i <= limit; i++) {
        let output = '';
        
        if (i % 3 === 0) {
            output += 'Fizz';
        }
        
        if (i % 5 === 0) {
            output += 'Buzz';
        }
        
        console.log(output || i);
    }
}

// Run FizzBuzz for numbers 1-20 as a demo
fizzbuzz(20);