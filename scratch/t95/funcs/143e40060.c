__int64 __fastcall sub_143E40060(_QWORD **a1, __int64 a2)
{
  _QWORD **v4; // rax
  _QWORD *v5; // rax
  unsigned __int64 v6; // r13
  __int64 v7; // rax
  __int64 v8; // rdx
  __int64 *v9; // rbx
  __int64 *v10; // rdx
  int v11; // eax
  __int64 v12; // rsi
  _QWORD **v13; // rax
  __int64 v14; // rcx
  _QWORD *v15; // rax
  __int64 v16; // rdi
  _QWORD **v17; // rax
  __int64 v18; // rcx
  _QWORD *v19; // rax
  __int64 v20; // rdi
  __int64 v21; // rax
  char v22; // bl
  __int64 v24; // rax
  char v25; // cl
  __int64 v26; // [rsp+20h] [rbp-10h] BYREF
  __int64 v27; // [rsp+28h] [rbp-8h]
  __int64 v28; // [rsp+30h] [rbp+0h]

  v28 = -2;
  v4 = (_QWORD **)(*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)**a1 + 96LL))(**a1);
  if ( v4 != nullptr && (v5 = *v4) != nullptr )
    v6 = (__int64)(v5[1] - *v5) >> 3;
  else
    v6 = 0;
  v7 = qword_141B60C30;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    v8 = qword_141B60C30;
    while ( *(_DWORD *)v8 != 1684171881 )
    {
      v8 += 16;
      if ( v8 == qword_141B60C38 )
        goto LABEL_26;
    }
    if ( v8 != qword_141B60C38 && *(_QWORD *)(v8 + 8) != 0 )
    {
      v9 = nullptr;
      while ( *(_DWORD *)v7 != 1684171881 )
      {
        v7 += 16;
        if ( v7 == qword_141B60C38 )
          goto LABEL_19;
      }
      v9 = v7 == qword_141B60C38 ? nullptr : *(__int64 **)(v7 + 8);
LABEL_19:
      v10 = &qword_141B5A4A0;
      if ( v9 != nullptr )
        v10 = v9;
      v11 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v10 + 64LL))(*v10);
      LODWORD(v12) = v11;
      if ( v11 >= 0 && v6 > (unsigned int)v11 )
      {
        v13 = (_QWORD **)(*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)**a1 + 96LL))(**a1);
        if ( v13 != nullptr && (v15 = *v13) != nullptr )
          v16 = *(_QWORD *)(*v15 + 8LL * (unsigned int)v12);
        else
          v16 = 0;
        v24 = sub_14083D4F0(v14) + 8;
        v27 = 0;
        v26 = v24;
        if ( v16 != 0 )
        {
          sub_140FEA6A0(v16, &v26);
          v25 = sub_140DD6070(a2, &v26, 0);
          v24 = v26;
          if ( v25 != 0 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v26 + 16LL))(v26, &v26);
            return (unsigned int)v12;
          }
        }
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v24 + 16LL))(v24, &v26);
LABEL_27:
        v12 = 0;
        while ( 1 )
        {
          v17 = (_QWORD **)(*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)**a1 + 96LL))(**a1);
          if ( v17 != nullptr && (v19 = *v17) != nullptr )
            v20 = *(_QWORD *)(*v19 + 8 * v12);
          else
            v20 = 0;
          v21 = sub_14083D4F0(v18) + 8;
          v27 = 0;
          v26 = v21;
          if ( v20 != 0 )
          {
            sub_140FEA6A0(v20, &v26);
            v22 = sub_140DD6070(a2, &v26, 0);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v26 + 16LL))(v26, &v26);
            if ( v22 != 0 )
              return (unsigned int)v12;
          }
          else
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v21 + 16LL))(v21, &v26);
          }
          if ( v6 == ++v12 )
            goto LABEL_37;
        }
      }
    }
  }
LABEL_26:
  if ( v6 != 0 )
    goto LABEL_27;
LABEL_37:
  LODWORD(v12) = -1;
  return (unsigned int)v12;
}
