import pygame


class GUI():
    def __init__(self,Stock,pnl,balance):
        self.stock = Stock
        self.pnl = pnl
        self.balance = balance
        
        pass
    def run(self):
        pygame.init()

        screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption("Fast SOOD")

        font = pygame.font.Font("Colleged.ttf", 32)
        info_label = font.render("Stock: {}".format(self.stock), True, "white")
        button_rect = pygame.Rect(150, 200, 100, 50) 
        

        TEXT_COLOR = (100, 100, 100)
        sell_image = pygame.image.load("SELL.png") 
        sell_rect = sell_image.get_rect(center=(1000, 150))
        buy_image = pygame.image.load("Buy.png") 
        buy_rect = buy_image.get_rect(center=(1100, 150))
        run = True
        while run:

          for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
              if buy_rect.collidepoint(event.pos):
                print("Buy Clicked") 
              if sell_rect.collidepoint(event.pos):
                print("Sell Clicked")  

          # Blit assets 

          screen.blit(info_label, (470, 30))
          screen.blit(buy_image, buy_rect)
          screen.blit(sell_image, sell_rect)

          pygame.display.update()

        pygame.quit()


R = GUI("AAPL",+1000,99999)
R.run()