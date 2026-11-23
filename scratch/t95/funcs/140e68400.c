char __fastcall sub_140E68400(_QWORD *a1, __int64 a2, __int64 a3)
{
  __int64 v6; // rdx
  __int64 v7; // rax
  __int64 v8; // rcx
  unsigned __int64 v9; // rsi
  __int64 v10; // rdx
  _QWORD *v11; // rax
  __int64 v12; // rax
  unsigned __int64 v13; // rdx
  int v14; // r9d
  __int128 v15; // kr00_16
  unsigned __int64 v16; // rsi
  __int64 v17; // rdx
  __int64 v18; // rax
  __int64 v19; // rcx
  unsigned __int64 v20; // rsi
  __int64 v21; // rdx
  __int64 *v22; // rax
  __int64 v23; // r8
  __int64 v24; // rax
  unsigned __int64 v25; // rcx
  __int64 v26; // rbx
  __int64 v27; // rsi
  signed __int32 v28; // et0
  __int128 v30; // [rsp+30h] [rbp-20h] BYREF
  __int64 v31; // [rsp+40h] [rbp-10h]
  __int64 v32; // [rsp+48h] [rbp-8h]

  v32 = -2;
  v6 = a1[41];
  if ( v6 != 0 )
    sub_140E688D0(a1, v6, a2, 0);
  v7 = a1[18];
  v8 = a1[19];
  if ( v8 != v7 )
  {
    v9 = 0;
    do
    {
      v10 = *(_QWORD *)(v7 + 8 * v9);
      if ( v10 != 0 )
      {
        sub_140E688D0(a1, v10, a2, a3);
        v7 = a1[18];
        v8 = a1[19];
      }
      ++v9;
    }
    while ( v9 < (v8 - v7) >> 3 );
  }
  v11 = (_QWORD *)a1[3];
  if ( v11 != (_QWORD *)a1[4] && *v11 != 0 )
  {
    v12 = sub_1411A41D0();
    if ( v12 != 0 )
      sub_140E688D0(a1, v12, a2, a3);
  }
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
  v30 = 0;
  v31 = 0;
  sub_1411E5400(a1, &v30, 0, 0);
  v15 = v30;
  if ( *((_QWORD *)&v30 + 1) != (_QWORD)v30 )
  {
    v16 = 0;
    do
    {
      v17 = *(_QWORD *)(v15 + 8 * v16);
      if ( v17 != 0 )
      {
        sub_140E688D0(a1, v17, a2, a3);
        v15 = v30;
      }
      ++v16;
      v13 = (__int64)(*((_QWORD *)&v15 + 1) - v15) >> 3;
    }
    while ( v16 < v13 );
  }
  v18 = a1[12];
  v19 = a1[13];
  if ( v19 != v18 )
  {
    v20 = 0;
    do
    {
      v21 = *(_QWORD *)(v18 + 8 * v20);
      if ( v21 != 0 )
      {
        sub_140E688D0(a1, v21, a2, a3);
        v18 = a1[12];
        v19 = a1[13];
      }
      ++v20;
      v13 = (v19 - v18) >> 3;
    }
    while ( v20 < v13 );
  }
  v22 = (__int64 *)a1[3];
  if ( v22 == (__int64 *)a1[4] )
    LODWORD(v23) = 0;
  else
    v23 = *v22;
  LOBYTE(v13) = -118;
  LOBYTE(v14) = 1;
  v24 = sub_1411D9CF0((_DWORD)a1, v13, v23, v14, 1);
  if ( v24 != 0 )
  {
    v24 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v24 + 1688LL))(v24);
    if ( v24 != 0 )
      LOBYTE(v24) = sub_140E688D0(a1, v24, a2, a3);
  }
  if ( (_QWORD)v30 != 0 )
  {
    v25 = v31 - v30;
    if ( v31 - (_QWORD)v30 == -1 )
    {
      v25 = *(unsigned int *)(v30 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_41:
        LOBYTE(v24) = MEMORY[0x141948990](v30 - *(unsigned int *)(qword_141ABD470 + 48));
        return v24;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_41;
    }
    v26 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v26) >> 3 <= v25 )
      goto LABEL_41;
    v27 = *(_QWORD *)(v26 + 8 * v25);
    if ( v27 == 0 )
      goto LABEL_41;
    MEMORY[0x1419475D8](v27 + 32, v30 - *(unsigned int *)(v27 + 120));
    if ( *(_BYTE *)(v27 + 72) != 0 )
    {
      v28 = _InterlockedDecrement((volatile signed __int32 *)(v27 + 64));
      LOBYTE(v24) = v28 != 0;
      if ( v28 != 0 )
        return v24;
    }
    else
    {
      LOBYTE(v24) = 0;
    }
    if ( *(_BYTE *)(v27 + 97) != 0 )
      LOBYTE(v24) = sub_1412D33C0(v27);
  }
  return v24;
}
