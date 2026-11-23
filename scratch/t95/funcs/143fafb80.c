char __fastcall sub_143FAFB80(__int64 a1, __int64 a2, __int64 a3, char a4, unsigned __int8 a5)
{
  __int64 v8; // rbp
  __int64 v10; // rcx
  unsigned int v11; // edx
  char v12; // al
  char v13; // r8
  int v14; // ebp

  v8 = a1 + 80;
  sub_140F7EC80(a3, a1 + 80, *(_QWORD *)(a3 + 8), a5, 1, 0);
  sub_140F7FD40(a3, a1 + 88, a5);
  if ( *(_BYTE *)(a1 + 160) == 0 && *(_QWORD *)v8 != 0 )
  {
    v10 = *(_QWORD *)(*(_QWORD *)v8 + 32LL);
    if ( v10 != 0 )
    {
      v11 = *(_DWORD *)(a1 + 108);
      v12 = 1;
      if ( (int)v11 >= 1001 )
      {
        v13 = *(_BYTE *)(v10 + 464);
        if ( v13 >= 7 )
        {
          v14 = *(char *)(a1 + 159);
          if ( (unsigned int)(v14 - 2) < 2 )
          {
            v12 = 2 - (v11 < 0x1388 || (unsigned __int8)v13 < 0xBu);
          }
          else if ( (unsigned int)(v14 - 4) >= 2 )
          {
            if ( v14 == 1 )
            {
              v12 = 2;
              if ( v11 >= 0x1388 && (unsigned __int8)v13 >= 0xBu )
                v12 = (v11 >= 0xD6D9 && (unsigned __int8)v13 >= 0x11u) + 3;
            }
          }
          else
          {
            v12 = (v11 >= 0x7530 && (unsigned __int8)v13 >= 0xBu) + 1;
          }
        }
      }
      *(_BYTE *)(a1 + 160) = v12;
    }
  }
  if ( a4 != 0 )
    sub_140F7EE40(a3, a1 + 128, *(_QWORD *)(a3 + 16), a5, 1, 0);
  return 1;
}
