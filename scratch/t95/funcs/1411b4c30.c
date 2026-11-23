char __fastcall sub_1411B4C30(int a1, __int64 *a2)
{
  __int64 v4; // rcx
  __int64 v5; // rax
  __int64 v6; // rcx
  char result; // al
  unsigned __int64 v8; // rcx
  __int64 v9; // rbx
  __int64 v10; // rsi
  signed __int32 v11; // et0
  __int128 v12; // [rsp+40h] [rbp-40h] BYREF
  __int64 v13; // [rsp+50h] [rbp-30h]
  __int64 v14; // [rsp+58h] [rbp-28h] BYREF
  __int64 v15; // [rsp+60h] [rbp-20h]
  int v16; // [rsp+6Ch] [rbp-14h] BYREF
  int v17; // [rsp+70h] [rbp-10h] BYREF
  int v18; // [rsp+78h] [rbp-8h] BYREF
  char v19; // [rsp+7Eh] [rbp-2h] BYREF
  char v20; // [rsp+7Fh] [rbp-1h] BYREF
  __int64 v21; // [rsp+80h] [rbp+0h]

  v21 = -2;
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
  v12 = 0;
  v13 = 0;
  v17 = 124518401;
  v18 = 124518401;
  v19 = 0;
  v20 = 0;
  sub_1411BDAD0(a1, 1099391468, (unsigned int)&v12, (unsigned int)&v17, (__int64)&v18, (__int64)&v19, (__int64)&v20);
  v16 = 0;
  sub_1415EB660(&v14, &v12, 0, &v16);
  v4 = *a2;
  if ( &v14 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v4 + 16LL))(v4, a2);
    v5 = v14;
    v6 = v15;
    a2[1] = v15;
    *a2 = v5;
    v4 = sub_14083D4F0(v6) + 8;
    v15 = 0;
    v14 = v4;
  }
  result = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v4 + 16LL))(v4, &v14);
  if ( (_QWORD)v12 != 0 )
  {
    v8 = v13 - v12;
    if ( v13 - (_QWORD)v12 == -1 )
    {
      v8 = *(unsigned int *)(v12 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        return MEMORY[0x141948990](v12 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      return MEMORY[0x141948990](v12 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v9 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v9) >> 3 <= v8 )
      return MEMORY[0x141948990](v12 - *(unsigned int *)(qword_141ABD470 + 48));
    v10 = *(_QWORD *)(v9 + 8 * v8);
    if ( v10 == 0 )
      return MEMORY[0x141948990](v12 - *(unsigned int *)(qword_141ABD470 + 48));
    MEMORY[0x1419475D8](v10 + 32, v12 - *(unsigned int *)(v10 + 120));
    if ( *(_BYTE *)(v10 + 72) != 0 )
    {
      v11 = _InterlockedDecrement((volatile signed __int32 *)(v10 + 64));
      result = v11 != 0;
      if ( v11 != 0 )
        return result;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v10 + 97) != 0 )
      return sub_1412D33C0(v10);
  }
  return result;
}
