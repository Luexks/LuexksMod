
-- Press Control-r in game to reload this file (when kEnableDevBindings = true)
-- all paths are relative to "data/audio/"


-- default event settings
{
   -- samples  = { { file1, file2 }, { file3, file4} }
   -- pick between file1 and file2, and between file3 and file4
   -- play both selected samples when event is triggered
   
   volume         = 1,          -- volume to play samples at (0 is silent)
   pitch          = 1,          -- pitch samples up and down
   pitchRandomize = 0.0,        -- increase or decrease pitch randomly by up to this amount

   rolloff        = 0.8,        -- 3d: how fast the sound attenuates
   minDist        = 100,        -- 3d: point it starts attenuating
   maxDist        = 9999999999, -- 3d: stops attenuating
   
   priority       = 0,          -- lower priorities will skip playback if there are too many sounds
   
   flags          = 0           -- special flags to control playback, connected with "|"
   --  stream:      load files while playing (set this for music tracks). No Polyphony
   --  music:       only play one music track at a time (with crossfading)
   --  loop:        loop event when finished playing
   --  round_robin: cycle through samples instead of picking randomly
   --  crosssync:   keep music offset when changing tracks
   --  cluster:     group event together with spacially nearby events and only play once
   --  cull_vol:    don't play event if volume <kSoundVolumeCull
   --  cull3d_vol:  don't start playing if calculated 3d vol is < kSound3DVolumeCull
}

-- settings for each event
-- event names ('e.g' ButtonPress) are hard coded in the game binary. 

{ 
	Sakalou={
		samples={"Sakalou.ogg"}
		priority=-2
		minDist=500
		pitchRandomize = 0.1
		flags=cluster|cull_vol|cull3d_vol
		volume=0.3
	}
	Aisifuci={
		samples={"Aisifuci-1.ogg""Aisifuci-2.ogg""Aisifuci-3.ogg""Aisifuci-3.ogg""Aisifuci-4.ogg""Aisifuci-5.ogg""Aisifuci-6.ogg""Aisifuci-7.ogg""Aisifuci-8.ogg"}
		priority=-2
		minDist=500
		pitchRandomize = 0
		flags=cluster|cull_vol|cull3d_vol
		volume=1
	}
}

