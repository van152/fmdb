bool __fastcall sub_144745CD0(_QWORD *a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v6; // rbx
  _DWORD v7[7]; // [rsp+2Ch] [rbp-1Ch] BYREF

  v7[0] = (a1[1] - *a1) >> 3;
  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v7, 4);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  if ( v7[0] != 0 )
  {
    v6 = 0;
    while ( (unsigned __int8)sub_140F82F50(*(_QWORD *)(*a1 + 8 * v6), a2) != 0 )
    {
      if ( ++v6 >= (unsigned __int64)v7[0] )
        return *(_DWORD *)(*a2 + 16LL) == 0;
    }
    return false;
  }
  return *(_DWORD *)(*a2 + 16LL) == 0;
}
