__int64 __fastcall sub_14154E600(int *a1, __int64 *a2)
{
  __int64 v3; // rcx
  __int64 v4; // rax
  __int64 v5; // rcx
  __int64 v6; // rax
  __int64 v7; // rdi
  __int64 v8; // rbx
  unsigned __int64 v9; // rsi
  int *v10; // rdi
  __int64 v11; // r14
  __int64 v12; // r15
  __int64 *v13; // rdx
  int v14; // esi
  __int64 v15; // rcx
  __int64 v16; // rax
  __int64 v17; // rcx
  __int64 v18; // rax
  int v19; // ecx
  int v20; // eax
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 v23; // rax
  __int64 v24; // rcx
  unsigned __int64 v25; // rax
  __int64 v26; // rcx
  __int64 *v28; // [rsp+20h] [rbp-60h]
  __int64 v29; // [rsp+28h] [rbp-58h] BYREF
  __int64 v30; // [rsp+30h] [rbp-50h]
  int *v31; // [rsp+40h] [rbp-40h]
  __int64 v32; // [rsp+48h] [rbp-38h] BYREF
  __int64 v33; // [rsp+50h] [rbp-30h]
  __int64 v34; // [rsp+58h] [rbp-28h] BYREF
  int v35; // [rsp+60h] [rbp-20h]
  __int64 v36; // [rsp+68h] [rbp-18h]
  unsigned __int64 v37; // [rsp+70h] [rbp-10h] BYREF
  _QWORD v38[9]; // [rsp+78h] [rbp-8h] BYREF

  v38[1] = -2;
  v31 = a1;
  sub_1407C9510(&v29);
  v28 = a2;
  v4 = sub_14083D4F0(v3);
  v35 = 1668052322;
  v34 = v4 + 56;
  sub_14083B5F0(&v29, &v34);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v34 + 16LL))(v34, &v34);
  v6 = sub_14083D4F0(v5);
  v35 = 1668641388;
  v34 = v6 + 56;
  sub_14083B5F0(&v29, &v34);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v34 + 16LL))(v34, &v34);
  sub_1407C9510(&v34);
  v7 = v29;
  v8 = v30;
  v9 = (v30 - v29) >> 3;
  if ( (v36 - v34) >> 4 < v9 )
  {
    if ( (unsigned __int64)(v30 - v29) >= 0x7FFFFFFFFFFFFFF9LL )
      sub_1400526C0(0x7FFFFFFFFFFFFFF9LL);
    sub_140837DD0(&v34, (v30 - v29) >> 3);
  }
  if ( v8 != v7 )
  {
    v10 = v31 + 2;
    v11 = 1;
    if ( v9 >= 2 )
      v11 = v9;
    v12 = 0;
    while ( 1 )
    {
      v13 = *(__int64 **)(v29 + 8 * v12);
      if ( v13 == nullptr )
        v13 = &qword_141B5A4A0;
      v14 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v13 + 80LL))(*v13);
      v16 = sub_14083D4F0(v15) + 8;
      v33 = 0;
      v32 = v16;
      if ( v14 == 1668641388 )
        break;
      if ( v14 == 1668052322 )
      {
        v18 = sub_140F7A940(qword_141B5FDB8, v31);
        if ( v18 != 0 )
        {
          v19 = *(_DWORD *)(v18 + 12);
          v20 = *(_DWORD *)(v18 + 16);
          if ( v20 == 0 )
            v20 = v19;
        }
        else
        {
          v19 = -1;
          v20 = -1;
        }
        v37 = __PAIR64__(v20, v19);
        sub_140FE72B0((int *)&v37, 1130589301, &v32);
LABEL_23:
        sub_140835380(&v34, v14, &v32);
        v16 = v32;
      }
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v16 + 16LL))(v16, &v32);
      if ( v11 == ++v12 )
        goto LABEL_25;
    }
    v21 = sub_14083D4F0(v17);
    v38[0] = 0;
    if ( v38 != (_QWORD *)v10 )
    {
      v22 = *(_QWORD *)v10;
      if ( *(_QWORD *)v10 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v22 - 4));
      v38[0] = v22;
    }
    v37 = v21 + 136;
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v32 + 16LL))(v32, &v32);
    v33 = v38[0];
    v32 = v37;
    v23 = sub_14083D4F0(v38[0]);
    v38[0] = 0;
    v37 = v23 + 8;
    (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)(v23 + 8) + 16LL))(v23 + 8, &v37);
    goto LABEL_23;
  }
LABEL_25:
  sub_14083DDA0(&v37, &v34);
  v24 = *v28;
  if ( &v37 != (unsigned __int64 *)v28 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v24 + 16LL))(v24, v28);
    v25 = v37;
    v26 = v38[0];
    v28[1] = v38[0];
    *v28 = v25;
    v24 = sub_14083D4F0(v26) + 8;
    v38[0] = 0;
    v37 = v24;
  }
  (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v24 + 16LL))(v24, &v37);
  sub_140833970(&v34);
  return sub_14083B0A0(&v29);
}
