__int64 __fastcall sub_141196DE0(_QWORD *a1, __int64 a2, __int64 *a3)
{
  __int64 v5; // rdi
  __int64 v6; // rbx
  unsigned __int64 v7; // rsi
  __int64 v8; // r14
  __int64 v9; // r12
  __int64 *v10; // rdx
  int v11; // edi
  __int64 v12; // rcx
  __int64 v13; // rax
  __int64 v14; // rcx
  int v15; // ebx
  __int64 v16; // rax
  __int64 *v17; // rbx
  int v18; // r15d
  __int64 v19; // rax
  __int64 v20; // rcx
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 v24; // [rsp+28h] [rbp-58h] BYREF
  __int64 v25; // [rsp+30h] [rbp-50h]
  __int64 v26[3]; // [rsp+40h] [rbp-40h] BYREF
  __int64 v27[2]; // [rsp+58h] [rbp-28h] BYREF
  __int64 v28; // [rsp+68h] [rbp-18h]
  __int64 v29; // [rsp+70h] [rbp-10h] BYREF
  __int64 v30; // [rsp+78h] [rbp-8h]
  __int64 v31; // [rsp+80h] [rbp+0h]

  v31 = -2;
  v28 = a2;
  sub_1407C9510(&v24);
  sub_141523E70(*a1, &v24);
  sub_1407C9510(v26);
  v5 = v24;
  v6 = v25;
  v7 = (v25 - v24) >> 3;
  if ( (v26[2] - v26[0]) >> 4 < v7 )
  {
    if ( (unsigned __int64)(v25 - v24) >= 0x7FFFFFFFFFFFFFF9LL )
      sub_1400526C0(0x7FFFFFFFFFFFFFF9LL);
    sub_140837DD0(v26, (v25 - v24) >> 3);
  }
  if ( v6 != v5 )
  {
    v8 = 1;
    if ( v7 >= 2 )
      v8 = v7;
    v9 = 0;
    while ( 1 )
    {
      v10 = *(__int64 **)(v24 + 8 * v9);
      if ( v10 == nullptr )
        v10 = &qword_141B5A4A0;
      v11 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v10 + 80LL))(*v10);
      v13 = sub_14083D4F0(v12) + 8;
      v27[1] = 0;
      v27[0] = v13;
      if ( v11 <= 1346793580 )
        break;
      if ( v11 > 1347905890 )
      {
        if ( v11 > 1348036418 )
        {
          if ( v11 != 1348036419 )
          {
            if ( v11 == 1348101959 )
              goto LABEL_48;
            if ( v11 != 1348101955 )
              goto LABEL_53;
          }
        }
        else if ( v11 != 1347905891 )
        {
          if ( v11 != 1347905901 && v11 != 1348036417 )
            goto LABEL_53;
          goto LABEL_48;
        }
        goto LABEL_46;
      }
      if ( v11 > 1347185004 )
      {
        if ( v11 == 1347185005 )
          goto LABEL_48;
        if ( v11 != 1347905347 )
        {
          if ( v11 != 1347905351 )
            goto LABEL_53;
          goto LABEL_48;
        }
        goto LABEL_46;
      }
      if ( v11 == 1346793581 )
        goto LABEL_48;
      if ( v11 == 1347176803 )
        goto LABEL_46;
LABEL_53:
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v13 + 16LL))(v13, v27);
      if ( v8 == ++v9 )
        goto LABEL_59;
    }
    if ( v11 > 1346792546 )
    {
      if ( v11 <= 1346792808 )
      {
        if ( v11 != 1346792547 )
        {
          if ( v11 == 1346792557 )
            goto LABEL_48;
          if ( v11 != 1346792803 )
            goto LABEL_53;
        }
        goto LABEL_46;
      }
      if ( v11 != 1346792809 )
      {
        if ( v11 == 1346792813 )
          goto LABEL_48;
        if ( v11 != 1346793571 )
          goto LABEL_53;
        goto LABEL_46;
      }
      v17 = a3;
      v18 = *(unsigned __int8 *)(v28 + 41);
      if ( (char)v18 <= 0 )
      {
        (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
          qword_141B5A4A0,
          &qword_141B5A4A0,
          &v29);
      }
      else
      {
        v19 = sub_14083D4F0(v14);
        LODWORD(v30) = v18;
        v29 = v19 + 40;
      }
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v27[0] + 16LL))(v27[0], v27);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v29 + 24LL))(v29, &v29, v27);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v29 + 16LL))(v29, &v29);
      a3 = v17;
LABEL_52:
      sub_140835380(v26, v11, v27);
      v13 = v27[0];
      goto LABEL_53;
    }
    if ( v11 <= 1346791277 )
    {
      if ( v11 != 1346789986 && v11 != 1346791267 )
        goto LABEL_53;
      goto LABEL_46;
    }
    switch ( v11 )
    {
      case 1346791278:
        goto LABEL_48;
      case 1346791779:
LABEL_46:
        v15 = *(_DWORD *)(v28 + 24);
        if ( v15 > 0 )
        {
LABEL_49:
          v16 = sub_14083D4F0(v14);
          LODWORD(v30) = v15;
          v29 = v16 + 40;
LABEL_51:
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v27[0] + 16LL))(v27[0], v27);
          (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v29 + 24LL))(v29, &v29, v27);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v29 + 16LL))(v29, &v29);
          goto LABEL_52;
        }
        break;
      case 1346791789:
LABEL_48:
        v15 = *(_DWORD *)(v28 + 20);
        if ( v15 > 0 )
          goto LABEL_49;
        break;
      default:
        goto LABEL_53;
    }
    (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
      qword_141B5A4A0,
      &qword_141B5A4A0,
      &v29);
    goto LABEL_51;
  }
LABEL_59:
  sub_14083DDA0(&v29, v26);
  v20 = *a3;
  if ( &v29 != a3 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v20 + 16LL))(v20, a3);
    v21 = v29;
    v22 = v30;
    a3[1] = v30;
    *a3 = v21;
    v20 = sub_14083D4F0(v22) + 8;
    v30 = 0;
    v29 = v20;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v20 + 16LL))(v20, &v29);
  sub_140833970(v26);
  return sub_14083B0A0(&v24);
}
