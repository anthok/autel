from argparse import ArgumentParser
import re
import os, os.path
import errno
import hexdump


# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else: raise

def safe_open_w(path):
  ''' 
  Open "path" for writing, creating any parent directories as needed.
  '''
  mkdir_p(os.path.dirname(path))
  return open(path, 'wb')


def is_valid_file(parser, arg):
  if not os.path.exists(arg):
      parser.error("The file %s does not exist!" % arg)
  else:
      return open(arg, 'rb')  # return an open file handle

def bytes_to_hex_str(byte_arr):
 return ' '.join('{:02x}'.format(x) for x in byte_arr)

def parseEntries(bdata, output_folder):
  filetransfer = b'\x22\x3C\x66\x69\x6C\x65\x74\x72\x61\x6E\x73\x66\x65\x72\x3E\x22' #"<filetransfer>"
  fileinfo = b'\x22\x3C\x66\x69\x6C\x65\x69\x6E\x66\x6F\x3E\x22' #"<fileinfo>"
  filecontent = b'\x22\x3C\x66\x69\x6C\x65\x63\x6F\x6E\x74\x65\x6E\x74\x3E\x22' #"<filecontent>"


  entries = 0
  while True:
    transfer_start = bdata.find(filetransfer)
    if transfer_start == -1:
      print('No more transfers')
      break

    print('Transfer #{}'.format(entries))
    bdata = bdata[transfer_start + len(filetransfer):]


    info_start = bdata.find(fileinfo)
    bdata = bdata[info_start + len(fileinfo):]
    field_size = bdata[:4]
    field_size_int = int.from_bytes(field_size,'big')
    unknown = bdata[4:8]
    bdata = bdata[8:]
    filename = bdata[:field_size_int]
    filename_str = filename.decode('ascii')
    print('--info')
    print("\t field_size: {}".format(str(field_size_int)))
    print("\t unknown: {}".format(bytes_to_hex_str(unknown)))
    print("\t name: {}".format(filename_str))
    bdata = bdata[field_size_int:]

    content_start = bdata.find(filecontent)
    bdata = bdata[content_start + len(filecontent):]
    field_size = bdata[:4]
    field_size_int = int.from_bytes(field_size,'big')
    unknown = bdata[4:8]
    bdata = bdata[8:]
    data = bdata[:field_size_int]
    print('--content')
    print("\t field_size: {}".format(str(field_size_int)))
    print("\t unknown: {}".format(bytes_to_hex_str(unknown)))

    with safe_open_w('{}/{}'.format(output_folder, filename_str)) as fh:
      fh.write(data)

    bdata = bdata[field_size_int:]
    entries+=1

def main():
  parser = ArgumentParser(description="autel drone firmware update extractor")
  parser.add_argument("-f", dest="filename", required=True,
                      help="firmware update file", metavar="FILE",
                      type=lambda x: is_valid_file(parser, x))

  parser.add_argument('-o', dest="output", help='output folder', required=True)

  args = parser.parse_args()

  bdata = args.filename.read()

  print('LOGO')
  parseEntries(bdata, args.output)

  args.filename.close()



if __name__ == '__main__':
  main()