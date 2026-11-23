__int64 __fastcall sub_143EE19A0(__int64 a1, __int64 *a2)
{
  unsigned __int64 v4; // rdi
  __int64 v5; // r13
  unsigned __int64 v6; // rcx
  __int64 v7; // rsi
  __int64 v8; // r14
  unsigned __int64 v9; // rcx
  __int64 v10; // rcx
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 v14; // r8
  __int64 v15; // r15
  __int64 v16; // rbx
  __int64 v17; // rsi
  __int64 v18; // rax
  __int64 *v19; // [rsp+20h] [rbp-30h]
  __int64 v20; // [rsp+28h] [rbp-28h] BYREF
  __int64 v21; // [rsp+30h] [rbp-20h]
  __int64 v22; // [rsp+38h] [rbp-18h]
  __int64 v23; // [rsp+40h] [rbp-10h] BYREF
  __int64 v24; // [rsp+48h] [rbp-8h]
  __int64 v25; // [rsp+50h] [rbp+0h]

  v25 = -2;
  sub_1407C9510(&v20);
  v4 = (__int16)((*(_QWORD *)(**(_QWORD **)a1 + 200LL) - *(_QWORD *)(**(_QWORD **)a1 + 192LL)) >> 4);
  v5 = v20;
  v6 = (v22 - v20) >> 3;
  v19 = a2;
  if ( v6 >= v4 )
  {
    if ( (*(_QWORD *)(**(_QWORD **)a1 + 200LL) - *(_QWORD *)(**(_QWORD **)a1 + 192LL)) << 44 >> 48 == 0 )
      goto LABEL_8;
    goto LABEL_19;
  }
  if ( ((*(_QWORD *)(**(_QWORD **)a1 + 200LL) - *(_QWORD *)(**(_QWORD **)a1 + 192LL)) & 0x80000LL) != 0 )
    sub_1400526C0(v6);
  v7 = v21;
  v8 = sub_1407E4490(qword_141ABD470, 8 * v4);
  sub_141758A00();
  if ( v20 != 0 )
  {
    v9 = v22 - v20;
    if ( v22 - v20 == -1 )
    {
      v9 = *(unsigned int *)(v20 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_17:
        MEMORY[0x141948990](v20 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_18;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_17;
    }
    v14 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v14) >> 3 > v9 )
    {
      v15 = *(_QWORD *)(v14 + 8 * v9);
      if ( v15 != 0 )
      {
        MEMORY[0x1419475D8](v15 + 32, v20 - *(unsigned int *)(v15 + 120));
        if ( (*(_BYTE *)(v15 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v15 + 64)) == 0)
          && *(_BYTE *)(v15 + 97) != 0 )
        {
          sub_1412D33C0(v15);
        }
        goto LABEL_18;
      }
    }
    goto LABEL_17;
  }
LABEL_18:
  v20 = v8;
  v21 = v8 + v7 - v5;
  v22 = v8 + 8 * v4;
LABEL_19:
  v16 = 0;
  do
  {
    v17 = *(_QWORD *)(**(_QWORD **)a1 + 192LL);
    if ( v17 != 0 )
    {
      v18 = sub_14083D4F0(v6);
      v24 = 0;
      v23 = v18 + 8;
      sub_141050200((v16 >> 28) + v17, &v23);
      sub_14083B5F0(&v20, &v23);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v23 + 16LL))(v23, &v23);
    }
    v16 += 0x100000000LL;
    --v4;
  }
  while ( v4 != 0 );
LABEL_8:
  sub_14083DB80(&v23, &v20);
  v10 = *v19;
  if ( &v23 != v19 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v10 + 16LL))(v10, v19);
    v11 = v23;
    v12 = v24;
    v19[1] = v24;
    *v19 = v11;
    v10 = sub_14083D4F0(v12) + 8;
    v24 = 0;
    v23 = v10;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v10 + 16LL))(v10, &v23);
  return sub_14083B0A0(&v20);
}
