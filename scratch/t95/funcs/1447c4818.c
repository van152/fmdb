__int64 __fastcall sub_1447C4818(_DWORD *a1)
{
  MEMORY[0x141947418](&unk_141AC5D28);
  while ( 1 )
  {
    if ( *a1 == 0 )
    {
      *a1 = -1;
      return MEMORY[0x141947608](&unk_141AC5D28);
    }
    if ( *a1 != -1 )
      break;
    sub_141750F00(100);
  }
  *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex) + 4LL) = dword_141A8F920;
  return MEMORY[0x141947608](&unk_141AC5D28);
}
