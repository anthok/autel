# autel extractor
by _anthok 
 
<br/>

Unpack firmware update packages for the Autel EVO.

<br/>
<br/>

An example of an unpacked firmware [`EVO_FW_V1.4.9`] can be found in the `extracted_sample` folder at the root of this repository. 


## Usage

`python autel_extractor.py -f <firmware> -o <output_dir>`

<br/>
**Note:** The firmware package is nested, but the tool does not currently unpack the nested levels for you. You will need to rerun the tool and change the `-f` flag to point to your newly unpacked image. You can tell if a file can be further unpacked by looking for `"<filetransfer>"` at the start of the file.

<br/>

## How it works

Below is the format for the EVO firmware update package.

An update package is segmented by using an XML like structure, but there is no ending tag. The `"` characters are not a typo, those are part of the structure. The highest level tag is a `filetransfer` and signifies the begging of a file entry. Next, a `fileinfo` will follow, this will include an 8 byte header, 0-4 are the field_size, 4-8 are currently unknown, 8-field_size will be the filename. The last component of the transfer is `filecontent`. Once again this will include an 8 byte header, 0-4 are the field_size, 4-8 are currently unknown. The remaining bytes, 8-field_size are the actual content of the file being transfered.

`"<filetransfer>"` 
<br/>
<br/>

`"<fileinfo>"`  
**field_size**: bytes 0-4, big endian  
**unknown**: bytes 4-8, ??, crc/timestamp maybe  
**data**: bytes 8-X, data  
<br/>
<br/>

`"<filecontent>"`  
**field_size**: bytes 0-4, big endian  
**unknown**: bytes 4-8, ??, crc/timestamp maybe  
**data**: bytes 8-X, data 
<br/>
<br/>

