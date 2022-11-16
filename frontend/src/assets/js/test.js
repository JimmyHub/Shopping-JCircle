
/*export function random_get(array,times){
    //array 要取亂數的目標陣列 times 取亂數的次數
    let array_r=[]
    let array_g=[]
    for(var i=0;i<array.length;i++){
        array_r[i]=i
    }
    while(array_g.length<times){
        let num=Math.floor(Math.random()*length)
        if(array_r[num] != undefined){
            array_g[array_g.length]=array_r[num]
            delete array_r[num]
        }
    }
    return array_g
}*/

export function random_get2(length,times){
    //array 要取亂數的目標陣列 times 取亂數的次數
     let array_r=[]
     if(length >0 ){
        for(var i=0;i<length;i++){
            array_r[i]=i
        }
        //產生亂數之後檢查是否有相同的數字
        let array_g=[]
        if(length < 4 ){
            times = length
        }
        while(array_g.length<times){
            let num=Math.floor(Math.random()*length)
            if(array_r[num] != undefined){
                array_g[array_g.length]=array_r[num]
                delete array_r[num]
            }
        }
        return array_g
     }else{
        return array_r
     }

    /*let array_g = [];
    let num = 0;
    var i = 0;
    var j = 0;
    let isDouble = true;
    for(i=0;i<times;i++){
      isDouble = true
      while(isDouble){
          num = Math.floor(Math.random() * length)
          console.log(num)
          if(array_g.length == 0){
            array_g[i] = num
            break
          }
          for(j = 0;j<array_g.length;j++){
            if(array_g[j] != num){
                isDouble = false
            }else{
                isDouble = true
                break
            }
          }        
      }
      array_g[i] = num
    }
    return array_g;*/
}