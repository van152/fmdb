__int64 __fastcall sub_1436763B0(
        __int64 a1,
        __int64 a2,
        int a3,
        unsigned int a4,
        char a5,
        char a6,
        int a7,
        unsigned __int64 a8)
{
  __int64 v12; // rdi
  unsigned int v13; // ecx
  unsigned __int64 v14; // r15
  int v15; // ebx
  unsigned int v16; // edx
  int v17; // r15d
  char v18; // al
  __int64 v19; // rsi
  __int64 v21; // [rsp+28h] [rbp-18h] BYREF
  __int64 v22; // [rsp+30h] [rbp-10h]
  int v23; // [rsp+38h] [rbp-8h] BYREF
  int v24; // [rsp+3Ch] [rbp-4h] BYREF
  __int64 v25; // [rsp+40h] [rbp+0h]

  v25 = -2;
  v12 = sub_141758DB0(a2) + 1;
  *(_QWORD *)a1 = sub_141751DE4(v12);
  sub_1417589F0();
  *(_QWORD *)(a1 + 8) = a8;
  *(_QWORD *)(a1 + 16) = 0;
  *(_QWORD *)(a1 + 24) = 0;
  *(_QWORD *)(a1 + 32) = 0;
  *(_QWORD *)(a1 + 40) = 0;
  *(_QWORD *)(a1 + 48) = 0;
  v13 = 8;
  if ( a4 >= 9 )
    v13 = a4;
  v14 = (a8 >> 9) & 0x7FF8;
  if ( v14 != 0 )
  {
    v15 = 0;
    v16 = v13 % (unsigned int)v14;
    v17 = v14 - v13 % (unsigned int)v14;
    if ( v16 != 0 )
      v15 = v17;
    v13 += v15;
  }
  *(_DWORD *)(a1 + 56) = v13;
  *(_DWORD *)(a1 + 60) = a3;
  *(_DWORD *)(a1 + 64) = a7;
  *(_DWORD *)(a1 + 68) = 100;
  *(_BYTE *)(a1 + 72) = a5;
  v22 = a1;
  *(_BYTE *)(a1 + 73) = a6;
  v23 = 0;
  v24 = 0;
  v18 = sub_1412D3E00(a2, &v23, &v24);
  v19 = v22;
  if ( v18 != 0 )
  {
    if ( v23 != 0 )
      *(_DWORD *)(v22 + 60) = v23;
    if ( v24 != 0 )
      *(_DWORD *)(v19 + 64) = v24;
  }
  if ( dword_141B59620 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B59620);
    if ( dword_141B59620 == -1 )
    {
      qword_141B595F0 = 0;
      qword_141B595E8 = 0;
      qword_141B595E0 = 0;
      qword_141B595D8 = 0;
      qword_141B595D0 = 0;
      qword_141B595C8 = 0;
      MEMORY[0x1419475B0](&unk_141B595F8);
      sub_141751048(sub_1407C2870);
      sub_141750EA0(&dword_141B59620);
    }
  }
  v21 = v19;
  MEMORY[0x141947418](&unk_141B595F8);
  if ( qword_141B595E8 == qword_141B595F0 )
  {
    sub_1407E4D40(&qword_141B595E0, qword_141B595E8, &v21);
  }
  else
  {
    *(_QWORD *)qword_141B595E8 = v19;
    qword_141B595E8 += 8;
  }
  MEMORY[0x141947608](&unk_141B595F8);
  return v19;
}
