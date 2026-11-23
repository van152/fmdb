char __fastcall sub_1411B4730(__int64 a1, __int64 *a2)
{
  __int64 v4; // rcx
  __int64 v5; // rax
  __int64 v6; // rcx
  char result; // al
  __int64 v8; // rdx
  __int128 v9; // rdi
  _QWORD *v10; // rbx
  __int64 v11; // rbx
  unsigned __int64 v12; // rcx
  __int64 v13; // rdx
  signed __int32 v14; // et0
  __int64 v15; // [rsp+20h] [rbp-30h] BYREF
  __int64 v16; // [rsp+28h] [rbp-28h]
  __int128 v17; // [rsp+30h] [rbp-20h] BYREF
  __int64 v18; // [rsp+40h] [rbp-10h]
  int v19; // [rsp+4Ch] [rbp-4h] BYREF
  __int64 v20; // [rsp+50h] [rbp+0h]

  v20 = -2;
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
  sub_1411BD330(a1, &v17);
  v19 = 0;
  sub_1415BD6E0(&v15, &v17, 0, &v19);
  v4 = *a2;
  if ( &v15 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v4 + 16LL))(v4, a2);
    v5 = v15;
    v6 = v16;
    a2[1] = v16;
    *a2 = v5;
    v4 = sub_14083D4F0(v6) + 8;
    v16 = 0;
    v15 = v4;
  }
  result = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v4 + 16LL))(v4, &v15);
  v9 = v17;
  if ( (_QWORD)v17 != *((_QWORD *)&v17 + 1) )
  {
    v10 = (_QWORD *)v17;
    do
    {
      if ( *v10 != 0 )
        sub_14102FEE0(*v10, v8);
      ++v10;
    }
    while ( v10 != *((_QWORD **)&v9 + 1) );
    v11 = *((_QWORD *)&v17 + 1) - *((_QWORD *)&v9 + 1);
    result = sub_141758A00();
    *((_QWORD *)&v17 + 1) = v9 + v11;
    *((_QWORD *)&v9 + 1) = v17;
  }
  if ( *((_QWORD *)&v9 + 1) != 0 )
  {
    v12 = v18 - *((_QWORD *)&v9 + 1);
    if ( v18 - *((_QWORD *)&v9 + 1) == -1 )
    {
      v12 = *(unsigned int *)(*((_QWORD *)&v9 + 1) - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        return MEMORY[0x141948990](*((_QWORD *)&v9 + 1) - *(unsigned int *)(qword_141ABD470 + 48));
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      return MEMORY[0x141948990](*((_QWORD *)&v9 + 1) - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v13 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v13) >> 3 <= v12 )
      return MEMORY[0x141948990](*((_QWORD *)&v9 + 1) - *(unsigned int *)(qword_141ABD470 + 48));
    *(_QWORD *)&v9 = *(_QWORD *)(v13 + 8 * v12);
    if ( (_QWORD)v9 == 0 )
      return MEMORY[0x141948990](*((_QWORD *)&v9 + 1) - *(unsigned int *)(qword_141ABD470 + 48));
    MEMORY[0x1419475D8](v9 + 32, *((_QWORD *)&v9 + 1) - *(unsigned int *)(v9 + 120));
    if ( *(_BYTE *)(v9 + 72) != 0 )
    {
      v14 = _InterlockedDecrement((volatile signed __int32 *)(v9 + 64));
      result = v14 != 0;
      if ( v14 != 0 )
        return result;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v9 + 97) != 0 )
      return sub_1412D33C0(v9);
  }
  return result;
}
