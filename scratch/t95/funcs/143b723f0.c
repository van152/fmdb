__int64 __fastcall sub_143B723F0(__int64 a1)
{
  __int64 v2; // rbx
  __int64 v3; // rax
  __int64 v4; // rcx
  unsigned int v5; // edi
  __int64 v6; // rax
  __int64 v7; // rax

  v2 = a1 - 336;
  v3 = *(_QWORD *)(a1 - 168);
  if ( v3 != 0 && (v4 = *(_QWORD *)(v3 + 16)) != 0 )
    v5 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v4 + 80LL))(v4);
  else
    v5 = 0;
  v6 = *(int *)(*(_QWORD *)(a1 - 328) + 4LL);
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)(a1 + v6 - 328) + 1296LL))(v6 + v2 + 8) != 0 )
  {
    v7 = *(int *)(*(_QWORD *)(a1 - 328) + 4LL);
    LOBYTE(v5) = ((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)(a1 + v7 - 328) + 640LL))(v7 + v2 + 8) != 0) | v5;
  }
  return v5;
}
