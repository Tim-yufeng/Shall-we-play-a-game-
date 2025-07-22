#include <stdio.h>
#include <stdlib.h>
extern int addAllDigits(int num);
int main(void){
    int num;
    printf("Hello world!\n");
    printf("Please enter an integer: ");
    scanf("%d",&num);
    int sum=addAllDigits(num);
    printf("%d",sum);

    return 0;
}
