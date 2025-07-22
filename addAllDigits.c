#include<stdio.h>
#include<math.h>
int addAllDigits(int num){
    int  result=0;
    while (num!=0){
         result+=num%10;
        num=(num-num%10)/10;
//        num=floor(num/10);
    }
//       printf("%d",result);
    return result;

}
