char __fastcall sub_143859620(__int64 a1, __int64 a2, _QWORD *a3)
{
  __int64 v4; // rax
  __int64 v5; // rdi
  _QWORD *v7; // rdi

  v4 = *(_QWORD *)(a1 + 1496);
  v5 = *(_QWORD *)(a1 + 1504);
  if ( v4 == v5 )
    goto LABEL_4;
  while ( *(_DWORD *)v4 != (_DWORD)a2 )
  {
    v4 += 16;
    if ( v4 == v5 )
      goto LABEL_4;
  }
  if ( v4 == v5 || (v7 = *(_QWORD **)(v4 + 8)) == nullptr )
  {
LABEL_4:
    sub_140835A40(a1 + 1496, a2, a3);
  }
  else if ( v7 != a3 )
  {
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*v7 + 16LL))(*v7, v7);
    (*(void (__fastcall **)(_QWORD, _QWORD *, _QWORD *))(*(_QWORD *)*a3 + 24LL))(*a3, a3, v7);
  }
  return 1;
}
