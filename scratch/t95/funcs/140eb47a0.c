__int64 __fastcall sub_140EB47A0(__int64 **a1, __int64 *a2)
{
  __int64 v4; // rsi
  __int64 v5; // rdi
  __int64 v6; // rdi
  _QWORD *v7; // rbx
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 v10; // rdx
  unsigned __int64 v11; // r12
  __int64 v12; // rdi
  __int64 v13; // rbx
  __int64 v14; // r13
  unsigned __int64 v15; // rcx
  __int64 v16; // r8
  __int64 v17; // rcx
  bool v18; // al
  __int64 v19; // rcx
  __int64 v20; // rax
  __int64 v21; // rcx
  __int64 v23; // rsi
  __int64 v24; // r13
  __int64 v25; // rdi
  __int64 v26; // rdi
  _QWORD *v27; // rbx
  __int64 v28; // rcx
  __int64 v29; // rbx
  __int64 v30; // rax
  __int64 v31; // [rsp+20h] [rbp-30h]
  __int64 v32; // [rsp+28h] [rbp-28h] BYREF
  __int64 v33; // [rsp+30h] [rbp-20h]
  unsigned __int64 v34; // [rsp+38h] [rbp-18h]
  __int64 v35; // [rsp+40h] [rbp-10h] BYREF
  __int64 v36; // [rsp+48h] [rbp-8h]
  __int64 v37; // [rsp+50h] [rbp+0h]

  v37 = -2;
  sub_1407C9510(&v32);
  v4 = **a1;
  v5 = *(_QWORD *)(*(_QWORD *)(v4 + 176) + 8LL) - **(_QWORD **)(v4 + 176);
  if ( v5 != 0 )
  {
    v6 = v5 >> 3;
    while ( 1 )
    {
      v7 = *(_QWORD **)(**(_QWORD **)(v4 + 176) + 8 * v6 - 8);
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD *))(*v7 + 56LL))(v7) == 38
        && (*(unsigned int (__fastcall **)(_QWORD *))(*v7 + 64LL))(v7) == -1
        && (*(unsigned int (__fastcall **)(_QWORD *))(*v7 + 72LL))(v7) == -1 )
      {
        break;
      }
      if ( --v6 == 0 )
        goto LABEL_18;
    }
    v8 = v7[1];
    v9 = v7[2];
    v10 = v9 - v8;
    v11 = (v9 - v8) >> 3;
    v12 = v32;
    if ( (__int64)(v34 - v32) >> 3 >= v11 )
    {
      if ( v9 == v8 )
        goto LABEL_18;
    }
    else
    {
      if ( v10 < 0 )
        sub_1400526C0(v9);
      v13 = v33;
      v14 = sub_1407E4490(qword_141ABD470, v10);
      sub_141758A00();
      if ( v32 != 0 )
      {
        v15 = v34 - v32;
        if ( v34 - v32 == -1 )
          v15 = *(unsigned int *)(v32 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v16 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v16) >> 3 > v15)
          && (v17 = *(_QWORD *)(v16 + 8 * v15)) != 0 )
        {
          v31 = v17;
          MEMORY[0x1419475D8](v17 + 32, v32 - *(unsigned int *)(v17 + 120));
          v18 = *(_BYTE *)(v31 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v31 + 64)) != 0;
          if ( !v18 && *(_BYTE *)(v31 + 97) != 0 )
            sub_1412D33C0(v31);
        }
        else
        {
          MEMORY[0x141948990](v32 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      v32 = v14;
      v33 = v14 + v13 - v12;
      v34 = v14 + 8 * v11;
    }
    v23 = 0;
    do
    {
      v24 = **a1;
      v25 = *(_QWORD *)(*(_QWORD *)(v24 + 176) + 8LL) - **(_QWORD **)(v24 + 176);
      if ( v25 != 0 )
      {
        v26 = v25 >> 3;
        while ( 1 )
        {
          v27 = *(_QWORD **)(**(_QWORD **)(v24 + 176) + 8 * v26 - 8);
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD *))(*v27 + 56LL))(v27) == 38
            && (*(unsigned int (__fastcall **)(_QWORD *))(*v27 + 64LL))(v27) == -1
            && (*(unsigned int (__fastcall **)(_QWORD *))(*v27 + 72LL))(v27) == -1 )
          {
            break;
          }
          if ( --v26 == 0 )
            goto LABEL_24;
        }
        v29 = *(_QWORD *)(v27[1] + 8 * v23);
        if ( v29 != 0 )
        {
          v30 = sub_14083D4F0(v28);
          v36 = 0;
          v35 = v30 + 8;
          sub_140EA4390(v29, &v35);
          sub_14083B5F0(&v32, &v35);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v35 + 16LL))(v35, &v35);
        }
      }
LABEL_24:
      ++v23;
    }
    while ( v23 != v11 );
  }
LABEL_18:
  sub_14083DB80(&v35, &v32);
  v19 = *a2;
  if ( &v35 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v19 + 16LL))(v19, a2);
    v20 = v35;
    v21 = v36;
    a2[1] = v36;
    *a2 = v20;
    v19 = sub_14083D4F0(v21) + 8;
    v36 = 0;
    v35 = v19;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v19 + 16LL))(v19, &v35);
  return sub_14083B0A0(&v32);
}
