__int64 __fastcall sub_14153D380(__int64 a1, int a2, unsigned __int64 *a3)
{
  __int64 v6; // rbx
  __int64 v7; // rax
  __int64 v8; // rcx
  __int64 v9; // rcx
  int v10; // eax
  unsigned __int64 *v11; // rcx
  __int64 v12; // rdx
  int v13; // esi
  __int64 v14; // rax
  unsigned __int64 v15; // rax
  unsigned __int64 v16; // rcx
  int v17; // ecx
  int v18; // eax
  int v19; // esi
  unsigned __int64 v20; // rax
  unsigned __int64 v21; // rcx
  int v22; // esi
  unsigned __int64 v23; // rax
  unsigned __int64 v24; // rcx
  __int64 v25; // rbx
  __int64 v26; // rsi
  unsigned __int64 v27; // rax
  unsigned __int64 v28; // rcx
  unsigned __int64 v29; // rax
  unsigned __int64 v30; // rcx
  __int64 v31; // rsi
  __int64 v32; // r15
  __int64 v33; // rax
  __int64 v34; // rax
  int v35; // ecx
  int v36; // eax
  unsigned __int64 v38; // [rsp+20h] [rbp-10h] BYREF
  unsigned __int64 v39; // [rsp+28h] [rbp-8h]
  __int64 v40; // [rsp+30h] [rbp+0h]

  v40 = -2;
  LODWORD(v6) = 0;
  v7 = sub_140FE84D0();
  if ( a2 > 1836345458 )
  {
    if ( a2 == 1836345459 )
    {
      v19 = *(_DWORD *)(a1 + 48);
      v14 = sub_14083D4F0(v8) + 40;
      LODWORD(v39) = v19;
      v38 = v14;
      if ( &v38 != a3 )
      {
        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v20 = v38;
        v21 = v39;
        a3[1] = v39;
        *a3 = v20;
        v14 = sub_14083D4F0(v21) + 8;
        v39 = 0;
        v38 = v14;
      }
      goto LABEL_35;
    }
    if ( a2 == 1887005046 )
    {
      v22 = *(char *)(a1 + 56);
      v14 = sub_14083D4F0(v8) + 40;
      LODWORD(v39) = v22;
      v38 = v14;
      if ( &v38 != a3 )
      {
        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v23 = v38;
        v24 = v39;
        a3[1] = v39;
        *a3 = v23;
        v14 = sub_14083D4F0(v24) + 8;
        v39 = 0;
        v38 = v14;
      }
      goto LABEL_35;
    }
    if ( a2 != 1886151033 )
      return (unsigned int)v6;
    v11 = (unsigned __int64 *)(a1 + 24);
    v12 = 1348825715;
LABEL_47:
    sub_140FE72B0(v11, v12, a3);
    goto LABEL_48;
  }
  switch ( a2 )
  {
    case 1667330920:
      v13 = *(_DWORD *)(a1 + 52);
      v14 = sub_14083D4F0(v8) + 40;
      LODWORD(v39) = v13;
      v38 = v14;
      if ( &v38 != a3 )
      {
        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v15 = v38;
        v16 = v39;
        a3[1] = v39;
        *a3 = v15;
        v14 = sub_14083D4F0(v16) + 8;
        v39 = 0;
        v38 = v14;
      }
      goto LABEL_35;
    case 1668052322:
      if ( v7 != 0 )
      {
        v17 = *(_DWORD *)(v7 + 12);
        LODWORD(v38) = v17;
        v18 = *(_DWORD *)(v7 + 16);
        if ( v18 == 0 )
          v18 = v17;
      }
      else
      {
        LODWORD(v38) = -1;
        v17 = -1;
        v18 = -1;
      }
      v6 = qword_141B5FDB8;
      HIDWORD(v38) = v18;
      if ( v17 == *(_DWORD *)(a1 + 32) && v18 == *(_DWORD *)(a1 + 36)
        || (v31 = a1 + 32,
            v32 = (*(__int64 (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)qword_141B5FDB8 + 32LL))(
                    qword_141B5FDB8,
                    &v38),
            v33 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v6 + 32LL))(v6, a1 + 32),
            v6 = qword_141B5FDB8,
            v32 == v33) )
      {
        v31 = a1 + 40;
      }
      v34 = sub_140F7A940(v6, v31);
      if ( v34 != 0 )
      {
        v35 = *(_DWORD *)(v34 + 12);
        v36 = *(_DWORD *)(v34 + 16);
        if ( v36 == 0 )
          v36 = v35;
      }
      else
      {
        v35 = -1;
        v36 = -1;
      }
      v38 = __PAIR64__(v36, v35);
      v11 = &v38;
      v12 = 1130589301;
      goto LABEL_47;
    case 1768124269:
      if ( v7 != 0 )
      {
        v9 = *(unsigned int *)(v7 + 12);
        LODWORD(v38) = *(_DWORD *)(v7 + 12);
        v10 = *(_DWORD *)(v7 + 16);
        if ( v10 == 0 )
          v10 = v9;
      }
      else
      {
        LODWORD(v38) = -1;
        v9 = 0xFFFFFFFFLL;
        v10 = -1;
      }
      v25 = qword_141B5FDB8;
      HIDWORD(v38) = v10;
      if ( (_DWORD)v9 == *(_DWORD *)(a1 + 40) && v10 == *(_DWORD *)(a1 + 44)
        || (v26 = (*(__int64 (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)qword_141B5FDB8 + 32LL))(
                    qword_141B5FDB8,
                    &v38)) == (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v25 + 32LL))(v25, a1 + 40) )
      {
        v14 = sub_14083D4F0(v9) + 40;
        LODWORD(v39) = 1;
        v38 = v14;
        if ( &v38 != a3 )
        {
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v29 = v38;
          v30 = v39;
          a3[1] = v39;
          *a3 = v29;
          v14 = sub_14083D4F0(v30) + 8;
          v39 = 0;
          v38 = v14;
        }
      }
      else
      {
        v14 = sub_14083D4F0(v9) + 40;
        LODWORD(v39) = 0;
        v38 = v14;
        if ( &v38 != a3 )
        {
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v27 = v38;
          v28 = v39;
          a3[1] = v39;
          *a3 = v27;
          v14 = sub_14083D4F0(v28) + 8;
          v39 = 0;
          v38 = v14;
        }
      }
LABEL_35:
      v6 = *(_QWORD *)v14;
      (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v14 + 16LL))(v14, &v38);
LABEL_48:
      LOBYTE(v6) = 1;
      break;
    default:
      break;
  }
  return (unsigned int)v6;
}
