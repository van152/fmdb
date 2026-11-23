char __fastcall sub_143F00000(__int64 a1, unsigned int a2, __int64 **a3)
{
  __int64 v6; // rcx
  __int64 *v7; // rax
  __int64 *v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rcx

  v6 = qword_141B60C30;
  v7 = nullptr;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    while ( *(_DWORD *)v6 != 1986359923 )
    {
      v6 += 16;
      if ( v6 == qword_141B60C38 )
        goto LABEL_8;
    }
    if ( v6 == qword_141B60C38 )
      v7 = nullptr;
    else
      v7 = *(__int64 **)(v6 + 8);
  }
LABEL_8:
  v8 = &qword_141B5A4A0;
  if ( v7 != nullptr )
    v8 = v7;
  if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v8 + 8LL))(*v8, v8) != 0 )
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v8 + 64LL))(*v8, v8);
  v9 = *(_QWORD *)(a1 + 368);
  if ( (unsigned __int8)sub_141045D50(v9, a2, a3) != 0 )
    return 1;
  v10 = *(_QWORD *)(v9 + 264);
  if ( v10 != 0 && (unsigned __int8)sub_141063F30(v10, a2, a3) != 0 )
    return 1;
  if ( (unsigned __int8)sub_140FE2700((_DWORD *)v9, a2, a3) != 0 )
    return 1;
  else
    return sub_141063F30(a1, a2, a3);
}
