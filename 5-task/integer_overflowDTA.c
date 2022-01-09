#include <stdio.h>
#include <stdlib.h>

int main()
{
	printf("Hello, which product do you want to buy?\n");
	printf("1) IPhone 12\n");
	printf("2) IPhone 12 Pro\n");
	printf("3) IPhone 12 Pro Max Max\n");

	int item_choice;
	scanf("%d", &item_choice); // Source1
	// makeTainted("item_choice");

	printf("Great device, how many?\n");
	int item_quantity;
	scanf("%d", &item_quantity); // Source2
	// makeTainted("item_quantity");

	if (item_quantity <= 0) {
		printf("You should buy at least one Iphone!\n");
		return -1;
	}

	int insurance = 1200;
	if (item_choice == 3)
	{
		// makeUntainted("item_choice");
		// if(isTainted("item_quantity") && isIntegerOverflowAttack(item_quantity) {
		//		return -1;
		// }		
		int price = 1500*item_quantity + insurance; // Sink1
		// makeCondTainted("price", ["item_quantity"]);
		if (price == 0) {
			printf("You solved the problem\n");
			printf("The Iphone Max Max is yours\n");
			return 1;
		}
		printf("You have to pay €%d\n", price);
	}
	else
	{
		if (item_quantity > 3) {
			printf("You can buy maximum 3\n");
			return -1;
		}
		// makeUntainted("item_quantity");
		// if(isTainted("item_quantity") && isIntegerOverflowAttack(item_quantity) {
		//		return -1;
		// }		
		int price = 1000*item_quantity; // Sink2
		// makeCondTainted("price", ["item_quantity"]);
		printf("You have to pay €%d\n", price);
	}
	return 0;
}
