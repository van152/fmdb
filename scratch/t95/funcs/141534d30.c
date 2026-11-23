_QWORD *__fastcall sub_141534D30(_QWORD *a1, __int64 a2, unsigned __int8 a3)
{
  int v6; // eax
  __int64 v7; // rcx
  unsigned __int8 v9; // bl
  unsigned __int64 v10; // rax
  __int64 v11; // rcx

  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  a1[2] = 0;
  a1[1] = 0;
  *a1 = 0;
  v6 = a3;
  if ( a3 <= 0x2Du )
  {
    v7 = 0x30000000C000LL;
    if ( _bittest64(&v7, a3) )
      goto LABEL_6;
  }
  v9 = a3 & 0xFE;
  if ( v9 <= 0x39u )
  {
    if ( v9 != 4 && v9 != 6 && v9 != 24 )
      goto LABEL_16;
LABEL_18:
    sub_141535250(a1, a2);
    return a1;
  }
  if ( v9 == 84 || v9 == 70 )
    goto LABEL_18;
  if ( v9 == 58 )
  {
LABEL_6:
    sub_141534EA0(a1, a2);
    return a1;
  }
LABEL_16:
  v10 = (unsigned int)(v6 - 8);
  if ( (unsigned int)v10 <= 0x3B )
  {
    v11 = 0xC00000000000003LL;
    if ( _bittest64(&v11, v10) )
      goto LABEL_18;
  }
  if ( v9 == 68 )
    goto LABEL_18;
  return a1;
}
