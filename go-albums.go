package main

import (
	//	"github.com/egonik-unlp/go-albums/spotify_auth"
	//	"github.com/zmb3/spotify"
	"fmt"
	"os"
	"strings"

	"github.com/egonik-unlp/go-albums/spotify_auth"
	"github.com/zmb3/spotify"
)

func main() {
	spotifyClient := spotify_auth.Authenticate()

	file, err := os.ReadFile("dump_albumes.txt")
	if err != nil {
		fmt.Println("cannot read album file")
	}
	str := string(file)
	for _, album := range strings.Split(str, "\n") {
		fmt.Println(album)
		dec_album := strings.SplitAfterN(album, "->", 2)

		album, _ := strings.CutSuffix(dec_album[0], "->")
		raw_id := strings.TrimSpace(dec_album[1])
		id, worked := strings.CutPrefix(raw_id, "spotify:track:")
		if !worked {
			continue
		}
		fmt.Printf("track_id %s\n", id)
		song, err := spotifyClient.GetTrack(spotify.ID(id))
		if err != nil {
			fmt.Println("Couldnt find track information")
		}
		fileName := fmt.Sprintf("dump/albumArt_%s.jpg", strings.TrimSpace(album))
		saveFile, err := os.Create(fileName)
		if err != nil {
			fmt.Printf("Cannot create image dump file %s", fileName)
		}
		// if err = jpeg.Encode(song.Album.Images[o]., saveFile, nil); err != nil {
		// 	fmt.Printf("failed to encode: %v", err)
		// }

		album_image := song.Album.Images[0]
		album_image.Download(saveFile)

	}
}
