__int64 __fastcall sub_143C333F0(__int64 a1, unsigned int a2)
{
  __int64 v4; // rsi
  __int64 v5; // rdi
  __int64 v6; // r15
  __int64 v7; // rdi
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 v10; // rbx
  unsigned int v11; // eax
  __int64 v12; // rcx
  unsigned __int64 v13; // rcx
  __int64 v14; // rbx
  __int64 v15; // rbx
  __int128 v17; // [rsp+20h] [rbp-20h] BYREF
  __int64 v18; // [rsp+30h] [rbp-10h]
  __int64 v19; // [rsp+40h] [rbp+0h]

  v19 = -2;
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
  v17 = 0;
  v18 = 0;
  v4 = 0;
  sub_1411E5770(a1, &v17, 0, a2);
  v5 = *((_QWORD *)&v17 + 1);
  if ( *((_QWORD *)&v17 + 1) != (_QWORD)v17 )
  {
    v6 = 1;
    if ( (unsigned __int64)((__int64)(*((_QWORD *)&v17 + 1) - v17) >> 3) >= 2 )
      v6 = (__int64)(*((_QWORD *)&v17 + 1) - v17) >> 3;
    v7 = 0;
    while ( 1 )
    {
      v4 = *(_QWORD *)(v17 + 8 * v7);
      if ( v4 != 0 )
      {
        v8 = sub_140DE1C70(*(int *)(*(_QWORD *)(v4 + 8) + 8LL) + v4 + 344, a1, 0);
        if ( v8 != 0 )
        {
          v10 = v8;
          LOBYTE(v9) = 64;
          if ( (unsigned __int8)sub_141033EF0(v9, *(unsigned __int8 *)(v8 + 28)) != 0 )
            break;
          v11 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v10 + 104LL))(v10);
          LOBYTE(v12) = 64;
          if ( (unsigned __int8)sub_141033EF0(v12, v11) != 0 )
            break;
        }
      }
      if ( v6 == ++v7 )
      {
        v4 = 0;
        break;
      }
    }
    v5 = v17;
  }
  if ( v5 != 0 )
  {
    v13 = v18 - v5;
    if ( v18 - v5 == -1 )
    {
      v13 = *(unsigned int *)(v5 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_26:
        MEMORY[0x141948990](v5 - *(unsigned int *)(qword_141ABD470 + 48));
        return v4;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_26;
    }
    v14 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v14) >> 3 <= v13 )
      goto LABEL_26;
    v15 = *(_QWORD *)(v14 + 8 * v13);
    if ( v15 == 0 )
      goto LABEL_26;
    MEMORY[0x1419475D8](v15 + 32, v5 - *(unsigned int *)(v15 + 120));
    if ( (*(_BYTE *)(v15 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v15 + 64)) == 0)
      && *(_BYTE *)(v15 + 97) != 0 )
    {
      sub_1412D33C0(v15);
    }
  }
  return v4;
}
