char __fastcall sub_14159BE20(_DWORD *a1, int a2, __int64 *a3)
{
  __int64 *v4; // rsi
  __int64 v5; // rax
  __int64 v6; // rcx
  __int64 v7; // rax
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 *v10; // rsi
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 v13; // rax
  __int64 v14; // rcx
  __int64 v15; // rcx
  __int64 v16; // rsi
  __int64 v17; // rdx
  __int64 v18; // r12
  __int64 v19; // rbx
  __int64 v20; // rbx
  __int64 v22; // rcx
  __int64 v23; // rdx
  unsigned __int64 v24; // rdi
  __int64 v25; // r15
  __int64 v26; // r13
  __int64 v27; // r14
  unsigned __int64 v28; // rcx
  __int64 v29; // r8
  __int64 v30; // rcx
  __int64 v31; // rsi
  bool v32; // al
  __int64 v33; // rbx
  __int64 i; // rdi
  __int64 v35; // r15
  __int64 v36; // rax
  int v37; // ecx
  __int64 v38; // rcx
  __int64 v39; // rax
  __int64 v40; // rcx
  unsigned __int64 v41; // rbx
  __int64 v42; // rcx
  __int64 v43; // rsi
  bool v44; // al
  unsigned __int64 v45; // rcx
  __int64 v46; // rbx
  __int64 v47; // rsi
  bool v48; // al
  __int64 *v49; // [rsp+20h] [rbp-60h]
  __int64 v50; // [rsp+28h] [rbp-58h] BYREF
  __int64 v51; // [rsp+30h] [rbp-50h]
  __int64 v52; // [rsp+38h] [rbp-48h]
  _DWORD v53[2]; // [rsp+40h] [rbp-40h] BYREF
  __int64 v54; // [rsp+48h] [rbp-38h]
  __int64 v55; // [rsp+50h] [rbp-30h]
  __int64 v56; // [rsp+58h] [rbp-28h] BYREF
  __int64 v57; // [rsp+60h] [rbp-20h]
  __int64 v58; // [rsp+68h] [rbp-18h] BYREF
  __int64 v59; // [rsp+70h] [rbp-10h] BYREF
  unsigned __int64 v60; // [rsp+78h] [rbp-8h]
  __int64 v61; // [rsp+80h] [rbp+0h]

  v61 = -2;
  switch ( a2 )
  {
    case 1097757801:
      sub_141735860(&v50, a1);
      v16 = v51 - v50;
      v17 = v51 - v50;
      v49 = a3;
      if ( v51 == v50 )
      {
        v18 = 0;
        v20 = 0;
        v54 = 0;
      }
      else
      {
        if ( v51 - v50 < 0 )
          sub_1400526C0(v15, v17);
        v18 = sub_1407E4490(qword_141ABD470, v17);
        v54 = v18 + 8 * (v16 >> 3);
        v19 = v51 - v50;
        sub_141758A00(v18, v50, v51 - v50);
        v20 = v18 + v19;
      }
      sub_1407C9510(&v58);
      v23 = v20 - v18;
      v24 = (v20 - v18) >> 3;
      v25 = v58;
      if ( (__int64)(v60 - v58) >> 3 < v24 )
      {
        if ( v23 < 0 )
          sub_1400526C0(v22, v23);
        v26 = v59;
        v27 = sub_1407E4490(qword_141ABD470, v23);
        sub_141758A00(v27, v58, v59 - v58);
        if ( v58 != 0 )
        {
          v28 = v60 - v58;
          if ( v60 - v58 == -1 )
            v28 = *(unsigned int *)(v58 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v29 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v29) >> 3 > v28)
            && (v30 = *(_QWORD *)(v29 + 8 * v28)) != 0 )
          {
            v31 = v58 - *(unsigned int *)(v30 + 120);
            v55 = v30;
            MEMORY[0x1419475D8](v30 + 32, v31);
            v22 = v55;
            v32 = *(_BYTE *)(v55 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v55 + 64)) != 0;
            if ( !v32 && *(_BYTE *)(v22 + 97) != 0 )
              sub_1412D33C0(v22);
          }
          else
          {
            MEMORY[0x141948990](v58 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        v58 = v27;
        v59 = v27 + v26 - v25;
        v60 = v27 + 8 * v24;
      }
      if ( v20 != v18 )
      {
        v33 = 1;
        if ( v24 >= 2 )
          v33 = v24;
        for ( i = 0; i != v33; ++i )
        {
          v35 = *(_QWORD *)(v18 + 8 * i);
          if ( v35 != 0 )
          {
            v36 = sub_14083D4F0(v22);
            v57 = 0;
            v56 = v36 + 8;
            v37 = *(_DWORD *)(v35 + 16);
            if ( v37 == 0 )
              v37 = *(_DWORD *)(v35 + 12);
            v53[0] = *(_DWORD *)(v35 + 12);
            v53[1] = v37;
            sub_140FE72B0(v53, 1315856756, &v56);
            sub_14083B5F0(&v58, &v56);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v56 + 16LL))(v56, &v56);
          }
        }
      }
      sub_14083DB80(&v56, &v58);
      v38 = *v49;
      if ( &v56 != v49 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v38 + 16LL))(v38, v49);
        v39 = v56;
        v40 = v57;
        v49[1] = v57;
        *v49 = v39;
        v38 = sub_14083D4F0(v40) + 8;
        v57 = 0;
        v56 = v38;
      }
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v38 + 16LL))(v38, &v56);
      sub_14083B0A0(&v58);
      if ( v18 != 0 )
      {
        v41 = v54 - v18;
        if ( v54 - v18 == -1 )
        {
          v41 = *(unsigned int *)(v18 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
          {
LABEL_55:
            MEMORY[0x141948990](v18 - *(unsigned int *)(qword_141ABD470 + 48));
            goto LABEL_56;
          }
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_55;
        }
        v42 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v42) >> 3 <= v41 )
          goto LABEL_55;
        v43 = *(_QWORD *)(v42 + 8 * v41);
        if ( v43 == 0 )
          goto LABEL_55;
        MEMORY[0x1419475D8](v43 + 32, v18 - *(unsigned int *)(v43 + 120));
        v44 = *(_BYTE *)(v43 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v43 + 64)) != 0;
        if ( !v44 && *(_BYTE *)(v43 + 97) != 0 )
          sub_1412D33C0(v43);
      }
LABEL_56:
      if ( v50 == 0 )
        return 1;
      v45 = v52 - v50;
      if ( v52 - v50 == -1 )
      {
        v45 = *(unsigned int *)(v50 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
LABEL_65:
          MEMORY[0x141948990](v50 - *(unsigned int *)(qword_141ABD470 + 48));
          return 1;
        }
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_65;
      }
      v46 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v46) >> 3 > v45 )
      {
        v47 = *(_QWORD *)(v46 + 8 * v45);
        if ( v47 != 0 )
        {
          MEMORY[0x1419475D8](v47 + 32, v50 - *(unsigned int *)(v47 + 120));
          v48 = *(_BYTE *)(v47 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v47 + 64)) != 0;
          if ( !v48 && *(_BYTE *)(v47 + 97) != 0 )
            sub_1412D33C0(v47);
          return 1;
        }
      }
      goto LABEL_65;
    case 1095201646:
      v10 = (__int64 *)(a1 + 10);
      v11 = sub_14083D4F0(a1);
      v59 = 0;
      if ( &v59 != v10 )
      {
        v12 = *v10;
        if ( *v10 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v12 - 4));
        v59 = v12;
      }
      v7 = v11 + 136;
      v58 = v7;
      if ( &v58 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v13 = v58;
        v14 = v59;
        a3[1] = v59;
        *a3 = v13;
        v7 = sub_14083D4F0(v14) + 8;
        v59 = 0;
        v58 = v7;
      }
      break;
    case 1095200353:
      v4 = (__int64 *)(a1 + 8);
      v5 = sub_14083D4F0(a1);
      v59 = 0;
      if ( &v59 != v4 )
      {
        v6 = *v4;
        if ( *v4 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v6 - 4));
        v59 = v6;
      }
      v7 = v5 + 136;
      v58 = v7;
      if ( &v58 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v8 = v58;
        v9 = v59;
        a3[1] = v59;
        *a3 = v8;
        v7 = sub_14083D4F0(v9) + 8;
        v59 = 0;
        v58 = v7;
      }
      break;
    default:
      return sub_140FE3F20(a1, a2, a3);
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v7 + 16LL))(v7, &v58);
  return 1;
}
