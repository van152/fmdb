__int64 __fastcall sub_143C82140(__int64 a1, __int64 *a2)
{
  __int64 *v4; // rcx
  __int64 v5; // rax
  __int64 v6; // rcx
  __int64 v7; // rdx
  unsigned __int64 v8; // rdi
  __int64 v9; // r14
  __int64 v10; // r15
  __int64 v11; // rbx
  unsigned __int64 v12; // rcx
  __int64 v13; // rcx
  __int64 v14; // rax
  __int64 v15; // rcx
  __int64 v17; // r8
  __int64 v18; // rcx
  __int64 v19; // r14
  __int64 *v20; // rax
  __int64 v21; // rsi
  __int64 v22; // rax
  __int64 *v23; // [rsp+28h] [rbp-38h]
  __int64 v24; // [rsp+30h] [rbp-30h]
  __int64 v25; // [rsp+38h] [rbp-28h] BYREF
  __int64 v26; // [rsp+40h] [rbp-20h]
  unsigned __int64 v27; // [rsp+48h] [rbp-18h]
  __int64 v28; // [rsp+50h] [rbp-10h] BYREF
  __int64 v29; // [rsp+58h] [rbp-8h]
  __int64 v30; // [rsp+60h] [rbp+0h]

  v30 = -2;
  sub_1407C9510(&v25);
  v4 = *(__int64 **)(*(_QWORD *)(**(_QWORD **)a1 + 256LL) + 40LL);
  if ( v4 == nullptr )
    v4 = &qword_141B5D9E8;
  v5 = *v4;
  v6 = v4[1];
  v7 = v6 - v5;
  v8 = (v6 - v5) >> 3;
  v9 = v25;
  v23 = a2;
  if ( (__int64)(v27 - v25) >> 3 >= v8 )
  {
    if ( v6 == v5 )
      goto LABEL_10;
    goto LABEL_21;
  }
  if ( v7 < 0 )
    sub_1400526C0(v6);
  v10 = v26;
  v11 = sub_1407E4490(qword_141ABD470, v7);
  sub_141758A00();
  if ( v25 != 0 )
  {
    v12 = v27 - v25;
    if ( v27 - v25 == -1 )
    {
      v12 = *(unsigned int *)(v25 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_19:
        MEMORY[0x141948990](v25 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_20;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_19;
    }
    v17 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v17) >> 3 > v12 )
    {
      v18 = *(_QWORD *)(v17 + 8 * v12);
      if ( v18 != 0 )
      {
        v24 = v18;
        MEMORY[0x1419475D8](v18 + 32, v25 - *(unsigned int *)(v18 + 120));
        v6 = v24;
        if ( (*(_BYTE *)(v24 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v24 + 64)) == 0)
          && *(_BYTE *)(v24 + 97) != 0 )
        {
          sub_1412D33C0(v24);
        }
        goto LABEL_20;
      }
    }
    goto LABEL_19;
  }
LABEL_20:
  v25 = v11;
  v26 = v11 + v10 - v9;
  v27 = v11 + 8 * v8;
LABEL_21:
  v19 = 0;
  do
  {
    v20 = *(__int64 **)(*(_QWORD *)(**(_QWORD **)a1 + 256LL) + 40LL);
    if ( v20 == nullptr )
      v20 = &qword_141B5D9E8;
    v21 = *(_QWORD *)(*v20 + 8 * v19);
    if ( v21 != 0 )
    {
      v22 = sub_14083D4F0(v6);
      v29 = 0;
      v28 = v22 + 8;
      sub_140EB0120(v21, &v28, 0);
      sub_14083B5F0(&v25, &v28);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v28 + 16LL))(v28, &v28);
    }
    ++v19;
  }
  while ( v8 != v19 );
LABEL_10:
  sub_14083DB80(&v28, &v25);
  v13 = *v23;
  if ( &v28 != v23 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v13 + 16LL))(v13, v23);
    v14 = v28;
    v15 = v29;
    v23[1] = v29;
    *v23 = v14;
    v13 = sub_14083D4F0(v15) + 8;
    v29 = 0;
    v28 = v13;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v13 + 16LL))(v13, &v28);
  return sub_14083B0A0(&v25);
}
