console.log('Hello guy')

function sum(...x){
    let s = 0;
    if (x.length < 2){
        return " Cannot find sum of one item"
    }
    for (let i=x.length; i>0 ; i--){
        let x1 = x.pop()
        if (Number(x1) == NaN){
            return `some of them items entered are not numbers`
        }
        s += x1
    }
    return s
}



function range(x, y, step = 1){
    let rng = [];

    if (x<y && step*-1===-step){
        console.log(step*-1)
        for(let i=0; x<=y; i++){

            rng.push(x), x+= step;
        };
    } else if (x>y && step*-1 !==-Math.abs(step)){
        console.log(`${step*-1} step*-1 , + 1 = ${(step*-1)+1}`)
        for (let i=x; x >=y; i--){
            console.log(x)
            rng.push(x), x-= Math.abs(step);
        };
    }
    if (x == y){
        return  "range(start, end), start s figure should not be equal tothe end!";
    }
    return rng;
}

//console.log(range(20, 2,-2))
let step =-1

console.log(step)
//console.log(sum(...range(1, 10)))