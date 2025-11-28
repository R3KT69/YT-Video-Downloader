import pygame
import pyperclip
import threading
from yt_dlp import YoutubeDL
from button import Button
import requests

pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 550

screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Video Downloader")


FPS = 30
WHITE = (255,255,255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
SKYBLUE = (135, 206, 235)
BACKGROUND = (25, 25, 25)
MUTED = (109, 89, 122)

inputFieldColor = WHITE
screen.fill(BACKGROUND)


video_title = ""
duration = ""
upload_date = ""
link_text = ""
thumbnail_url = ""
uploader = ""

font1 = pygame.font.Font(None, 25)
pTexts = pygame.font.Font(None, 25)
bigText = pygame.font.Font(None, 35)

fetchBtn = Button(25,100 + 25, 100, 75, SKYBLUE, "Fetch")     
pasteBtn = Button(25,100 + 125, 100, 75, SKYBLUE, "Paste")
copyBtn = Button(25,100 + 225, 100, 75, SKYBLUE, "Copy")
downloadBtn = Button(25,100 + 325, 100, 75, GREEN, "Download")

bVBtn = Button(148, 320, 110, 50, BLUE, "Best Quality")
wVBtn = Button(148, 380, 110, 50, RED, "Low Quality")
audioBtn = Button(148, 440, 110, 50, MUTED, "Audio")

delBtn = Button(SCREEN_WIDTH-50, 25 , 50, 25, RED, "[DEL]")

InputField = pygame.Rect(0,0, SCREEN_WIDTH, 50)  
VideoThumbnail = pygame.Rect(SCREEN_WIDTH-325,SCREEN_HEIGHT-225, 300, 200) 
DownloadField = pygame.Rect(137,SCREEN_HEIGHT-245, 125, 190)

image = pygame.image.load("thumbnails/template.jpg")
image = pygame.transform.scale(image, (VideoThumbnail.width, VideoThumbnail.height))

Fetching = False
ClickedDownload = False


def fetch_video(url, on_done=None):
    global video_title, duration, upload_date, uploader, thumbnail_url, Fetching
    Fetching = True
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_title = info["title"]
        duration = info["duration"]
        upload_date = info["upload_date"]
        uploader = info["uploader"]
        thumbnail_url = info["thumbnail"]
    if on_done:
        on_done()
        
def on_fetch_complete():
    global image, Fetching
    Fetching = False
    print("Fetch complete! Title is:", video_title)
    response = requests.get(thumbnail_url)
    if response.status_code == 200:
        with open("thumbnails/thumbnail.jpg", "wb") as f:
            f.write(response.content)
        print("Thumbnail saved as thumbnail.jpg")
    else:
        print("Failed to download thumbnail")
    image = pygame.image.load("thumbnails/thumbnail.jpg")
    image = pygame.transform.scale(image, (VideoThumbnail.width, VideoThumbnail.height))

def download_best(url):
    print("Downloading Best Quality...")
    ydl_opts = {
        "format": "best[ext=mp4]/best",                 
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "merge_output_format": "mp4"
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Best quality download complete!")

def download_low(url):
    print("Downloading Low Quality...")
    ydl_opts = {
        "format": "worst",                    
        "outtmpl": "downloads/%(title)s.%(ext)s"
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Low quality download complete!")

def download_audio(url):
    print("Downloading Audio (No FFmpeg)...")
    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "postprocessors": []  # no conversion
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Audio download complete!")


running = True
while running:
    screen.fill(BACKGROUND)
    mouseX, mouseY = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                link_text = link_text[:-1]
            elif event.key == pygame.K_p:
                link_text += pyperclip.paste()
                print(link_text)    
            else:
                link_text += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(f"Clicked on X:{mouseX} Y:{mouseY}")
                if fetchBtn.IsInside(mouseX, mouseY) and not Fetching:
                    print("ClickedButtonFetch")
                    if len(link_text) > 0:
                        inputFieldColor = GREEN
                        threading.Thread(target=fetch_video, args=(link_text,on_fetch_complete), daemon=True).start()
                           
                        
                        
                if pasteBtn.IsInside(mouseX, mouseY):
                    print("ClickedButtonPaste")
                    link_text = ""
                    link_text += pyperclip.paste()
                if copyBtn.IsInside(mouseX, mouseY):
                    pyperclip.copy(link_text)
                    print("ClickedButtonCpy")
                if delBtn.IsInside(mouseX, mouseY):
                    print("ClickedButtonDel")
                    link_text = ""
                    inputFieldColor = WHITE
                if downloadBtn.IsInside(mouseX, mouseY):
                    print("ClickedButtonDownload")
                    ClickedDownload = not ClickedDownload
                    print(ClickedDownload)
                if bVBtn.IsInside(mouseX, mouseY):
                    if ClickedDownload:
                        threading.Thread(target=download_best, args=(link_text,), daemon=True).start()

                if wVBtn.IsInside(mouseX, mouseY):
                    if ClickedDownload:
                        threading.Thread(target=download_low, args=(link_text,), daemon=True).start()

                if audioBtn.IsInside(mouseX, mouseY):
                    if ClickedDownload:
                        threading.Thread(target=download_audio, args=(link_text,), daemon=True).start()

                    
                    
            

            
            
            
    pygame.draw.rect(screen, inputFieldColor, InputField) 
    screen.blit(image, (VideoThumbnail.x, VideoThumbnail.y))    

    link_text_surface = pTexts.render("Link:" + link_text, True, BLACK)
    screen.blit(link_text_surface, (12.5,15))
    
    link_text_surface = bigText.render("Youtube Video Downloader", True, WHITE)
    screen.blit(link_text_surface, (90,75))

    link_text_surface = pTexts.render("Title: "+ str(video_title), True, WHITE)
    screen.blit(link_text_surface, (175,129))

    link_text_surface = pTexts.render("Uploader: " + str(uploader), True, WHITE)
    screen.blit(link_text_surface, (175,173))

    link_text_surface = pTexts.render("Date:" + str(upload_date), True, WHITE)
    screen.blit(link_text_surface, (175,214))

    link_text_surface = pTexts.render(f"Duration: {str(duration)}", True, WHITE)
    screen.blit(link_text_surface, (175,253))

    link_text_surface = pTexts.render("Thumbnail", True, WHITE)
    screen.blit(link_text_surface, (270,295))
    
    
    
    fetchBtn.DrawButton(screen, font1)
    pasteBtn.DrawButton(screen, font1)
    copyBtn.DrawButton(screen, font1)
    delBtn.DrawButton(screen, font1)
    downloadBtn.DrawButton(screen, font1)
    
    
    #print(mouseX, mouseY)

    if ClickedDownload: 
        pygame.draw.rect(screen, BACKGROUND, DownloadField)
        bVBtn.DrawButton(screen, font1)
        wVBtn.DrawButton(screen, font1)
        audioBtn.DrawButton(screen, font1)
    #pygame.draw.rect(screen, MUTED, DownloadField)     
     
      
    

    pygame.display.flip()
    clock.tick(FPS)
    



    

    

    

