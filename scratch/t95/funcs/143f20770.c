__int64 __fastcall sub_143F20770(__int64 a1, __int64 *a2)
{
  __int64 v4; // rcx
  __int64 v5; // r13
  __int64 v6; // r15
  __int64 v7; // rsi
  __int64 v8; // rbx
  unsigned __int64 v9; // rcx
  __int64 v10; // rcx
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 v14; // r8
  __int64 v15; // rcx
  __int64 v16; // rdi
  __int64 v17; // rsi
  __int64 v18; // rax
  __int64 v19; // [rsp+20h] [rbp-30h]
  __int64 v20; // [rsp+28h] [rbp-28h] BYREF
  __int64 v21; // [rsp+30h] [rbp-20h]
  __int64 v22; // [rsp+38h] [rbp-18h]
  __int64 v23; // [rsp+40h] [rbp-10h] BYREF
  __int64 v24; // [rsp+48h] [rbp-8h]
  __int64 v25; // [rsp+50h] [rbp+0h]

  v25 = -2;
  sub_1407C9510(&v20);
  v4 = (unsigned int)(*(_DWORD *)(**(_QWORD **)a1 + 1768LL) - *(_DWORD *)(**(_QWORD **)a1 + 1760LL)) >> 3;
  v5 = (unsigned __int16)v4;
  v6 = v20;
  if ( (v22 - v20) >> 3 >= (unsigned __int64)(unsigned __int16)v4 )
  {
    if ( (_WORD)v4 == 0 )
      goto LABEL_7;
    goto LABEL_18;
  }
  v7 = v21;
  v8 = sub_1407E4490(qword_141ABD470, 8LL * (unsigned __int16)v4);
  sub_141758A00();
  if ( v20 != 0 )
  {
    v9 = v22 - v20;
    if ( v22 - v20 == -1 )
    {
      v9 = *(unsigned int *)(v20 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_16:
        MEMORY[0x141948990](v20 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_17;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_16;
    }
    v14 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v14) >> 3 > v9 )
    {
      v15 = *(_QWORD *)(v14 + 8 * v9);
      if ( v15 != 0 )
      {
        v19 = v15;
        MEMORY[0x1419475D8](v15 + 32, v20 - *(unsigned int *)(v15 + 120));
        v4 = v19;
        if ( (*(_BYTE *)(v19 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v19 + 64)) == 0)
          && *(_BYTE *)(v19 + 97) != 0 )
        {
          sub_1412D33C0(v19);
        }
        goto LABEL_17;
      }
    }
    goto LABEL_16;
  }
LABEL_17:
  v20 = v8;
  v21 = v8 + v7 - v6;
  v22 = v8 + 8 * v5;
LABEL_18:
  v16 = 0;
  do
  {
    v17 = *(_QWORD *)(*(_QWORD *)(**(_QWORD **)a1 + 1760LL) + 8 * v16);
    if ( v17 != 0 )
    {
      v18 = sub_14083D4F0(v4);
      v24 = 0;
      v23 = v18 + 8;
      sub_141078520(v17, &v23);
      sub_14083B5F0(&v20, &v23);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v23 + 16LL))(v23, &v23);
    }
    ++v16;
  }
  while ( v5 != v16 );
LABEL_7:
  sub_14083DB80(&v23, &v20);
  v10 = *a2;
  if ( &v23 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v10 + 16LL))(v10, a2);
    v11 = v23;
    v12 = v24;
    a2[1] = v24;
    *a2 = v11;
    v10 = sub_14083D4F0(v12) + 8;
    v24 = 0;
    v23 = v10;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v10 + 16LL))(v10, &v23);
  return sub_14083B0A0(&v20);
}
